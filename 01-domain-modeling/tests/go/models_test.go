package main

import (
    "errors"
    "sort"
    "time"
    "testing"
    "github.com/stretchr/testify/assert"
)

type Batch struct {
    Reference   string      `json:"reference"`  
    Sku         string      `json:"sku"`        
    Qty         int         `json:"qty"`        
    Eta         *time.Time  // Nullable
    Allocations []OrderLine `json:"allocations"`
}

type OrderLine struct {
    Reference  string `json:"id"` 
    Sku string `json:"sku"`
    Qty int    `json:"qty"`
}

type Order struct {
    Reference  string      `json:"reference"` 
    OrderLines []OrderLine `json:"orderLines"`
}

func (batch *Batch) Equal(other Batch) bool {
    return batch.Reference == other.Reference
}

type Batches []*Batch
func (a Batches) Len() int           { return len(a) }
func (a Batches) Less(i, j int) bool { 
    if a[i].Eta == nil { return true }
    if a[j].Eta == nil { return false }
    return a[i].Eta.Before(*a[j].Eta)
}
func (a Batches) Swap(i, j int)      { a[i], a[j] = a[j], a[i] }

func (batch *Batch) AllocatedQty() int {
    sum := 0
    for _, line := range batch.Allocations { sum += line.Qty }
    return sum
}

func (batch *Batch) AvailableQty() int {
    return batch.Qty - batch.AllocatedQty()
}

func (batch *Batch) Allocate(line OrderLine) {
    if batch.CanAllocate(line) {
        batch.Allocations = append(batch.Allocations, line)
    }
}

func (batch *Batch) Deallocate(line OrderLine) {
    remains := []OrderLine {}
    for _, l := range batch.Allocations {
        if l == line {
            remains = append(remains, line)
        }
    }
    batch.Allocations = remains
}

func (batch *Batch) CanAllocate(line OrderLine) bool {
    return batch.Sku == line.Sku && batch.AvailableQty() >= line.Qty;
}

func Allocate(line OrderLine, batches []*Batch) string {
    sort.Sort(Batches(batches))
    availBatches := []*Batch{}
    for _, b := range batches {
        if b.CanAllocate(line) {
            availBatches = append(availBatches, b)
        }
    }
    if len(availBatches) == 0 {
        panic(errors.New("out of stock!"))
    }
    batch := availBatches[0]
    batch.Allocate(line)
    return batch.Reference
}

// Utility functions
func getDate(t time.Time) time.Time {
    return time.Date(t.Year(), t.Month(), t.Day(), 0, 0, 0, 0, time.Local)
}

func makeBatchAndLine(sku string, batchQty int, lineQty int) (Batch, OrderLine) {
    today := getDate(time.Now())
    return Batch { Reference: "batch-001", Sku: sku, Qty: batchQty, Eta: &today },
           OrderLine { Reference: "order-123", Sku: sku, Qty: lineQty }
}

func makeBatch(reference string, sku string, qty int, eta *time.Time) Batch {
    return Batch { Reference: reference, Sku: sku, Qty: qty, Eta: eta }
}

func makeOrderLine(reference string, sku string, qty int) OrderLine {
    return OrderLine { Reference: reference, Sku: sku, Qty: qty }
}

// fixtures

type DateFixture struct {
    today    time.Time
    tomorrow time.Time
    later    time.Time
} 

type TestFixture struct {
    dates    DateFixture
}

func SetupTest() TestFixture {
    today := getDate(time.Now())
    
    return TestFixture {
            dates: DateFixture {
            today: today, 
            tomorrow: today.Add(time.Hour * 24), 
            later: today.Add(time.Hour * 24 * 30),
        },
    }
}

// test_allocating_to_a_batch_reduces_the_available_quantity
func TestAllocatingToBatchReducesAvailableQuantity(t *testing.T) {
    dates := SetupTest().dates
    batch := Batch { Reference: "batch-001", Sku: "SMALL-TABLE", Qty: 20, Eta: &dates.today }
    line1 := OrderLine { Reference: "order-001", Sku: "SMALL-TABLE", Qty: 1 }
    line2 := OrderLine { Reference: "order-002", Sku: "SMALL-TABLE", Qty: 1 }
    batch.Allocate(line1)
    batch.Allocate(line2)
    assert.Equal(t, 18, batch.AvailableQty())
}

// test_can_allocate_if_available_greater_than_required
func TestCanAllocateIfAvailableGreaterThanRequired(t *testing.T) {
    largeBatch, smallLine := makeBatchAndLine("ELEGANT-LAMP", 20, 2);
    assert.True(t, largeBatch.CanAllocate(smallLine))
}

// test_cannot_allocate_if_available_smaller_than_required
func TestCannotAllocateIfAvailableSmallerThanRequired(t *testing.T) {
    smallBatch, largeLine := makeBatchAndLine("ELEGANT-LAMP", 2, 20)
    assert.False(t, smallBatch.CanAllocate(largeLine))
}

// test_can_allocate_if_available_equal_to_required
func TestCanAllocateIfAvailableEqualToRequired(t *testing.T) {
    batch, line := makeBatchAndLine("ELEGANT-LAMP", 2, 2)
    assert.True(t, batch.CanAllocate(line))
}

// test_prefers_warehouse_batches_to_shipments
func TestPrefersWarehouseBatchesToShipments(t *testing.T) {
    dates := SetupTest().dates
    warehouseBatch := makeBatch("warehouse-batch", "RETRO-CLOCK", 100, nil)
    shipmentBatch  := makeBatch("shipment-batch", "RETRO-CLOCK", 100, &dates.tomorrow)
    line := OrderLine { Reference: "oref", Sku: "RETRO-CLOCK", Qty: 10 }

    batchRef := Allocate(line, []*Batch{ &warehouseBatch, &shipmentBatch })
    assert.Equal(t, "warehouse-batch", batchRef)

    assert.Equal(t, 90, warehouseBatch.AvailableQty())
    assert.Equal(t, 100, shipmentBatch.AvailableQty())
}

// test_prefers_earlier_batches():
func TestPrefersEarlierBatches(t *testing.T) {
    dates := SetupTest().dates
    earliest := makeBatch("speedy-batch", "MINIMALIST-SPOON", 100, &dates.today)
    medium := makeBatch("normal-batch", "MINIMALIST-SPOON", 100, &dates.tomorrow)
    latest := makeBatch("slow-batch", "MINIMALIST-SPOON", 100, &dates.later)
    line := OrderLine { Reference: "order-001", Sku: "MINIMALIST-SPOON", Qty: 10 }

    batchRef := Allocate(line, []*Batch { &medium, &earliest, &latest })
    assert.Equal(t, "speedy-batch", batchRef)

    assert.Equal(t, 90, earliest.AvailableQty())
    assert.Equal(t, 100, medium.AvailableQty())
    assert.Equal(t, 100,latest.AvailableQty())
}

// test_raises_out_of_stock_exception_if_cannot_allocate
func TestRaisesOutOfStockExceptionIfCannotAllocate(t *testing.T) {
    dates := SetupTest().dates
    batch := makeBatch("batch1", "SMALFORK", 10, &dates.today)
    
    defer func() {
        if err := recover(); err != nil {
            assert.Equal(t, "out of stock!", err.(error).Error())
        }
    }()
    
    Allocate(makeOrderLine("order1", "SMALL-FORK", 10), []*Batch{ &batch })
    Allocate(makeOrderLine("order2", "SMALL-FORK", 1), []*Batch{ &batch })

}


