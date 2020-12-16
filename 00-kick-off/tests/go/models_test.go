package main

import (
    "time"
    "testing"
    "github.com/stretchr/testify/assert"
)

type Batch struct {
    Allocations []OrderLine
    Eta         time.Time
    Qty         int
    Reference   string
    Sku         string
}

type OrderLine struct {
    ID  string
    Qty int
    Sku string
}

type Order struct {
    OrderLines []OrderLine
    Reference  string
}

Batch { Sku: "TEST", }

func GetDate(t time.Time) time.Time {
    return time.Date(t.Year(), t.Month(), t.Day(), 0, 0, 0, 0, time.Local)
}

func makeBatchAndLine(sku string, batchQty int, lineQty int) (Batch, OrderLine) {
    today := GetDate(time.Now())
    return Batch { Reference: "batch-001", Sku: sku, Qty: batchQty, Eta: today },
           OrderLine { ID: "order-123", Sku: sku, Qty: lineQty }
}

func (batch *Batch) Allocate(line OrderLine) {
    batch.Allocations = append(batch.Allocations, line)
}

func (batch *Batch) AvailableQty() int {
    return 0
}

func TestAllocatingToBatchReducesAvailableQuantity(t *testing.T) {
    today := GetDate(time.Now())
    batch := Batch { Reference: "batch-001", Sku: "SMALL-TABLE", Qty: 20, Eta: today }
    line := OrderLine { ID: "order-ref", Sku: "SMALL-TABLE", Qty: 2 }
    batch.Allocate(line)
    assert.Equal(t, 0, batch.AvailableQty())
}

import (
    "fmt"
    "bytes"
    "os/exec"
)

func Test() {
    cmd := exec.Command(
        "jupyter", 
        "nbconvert", 
        "01. domain-modeling-go.ipynb",
        "--to=script",
        "--TagRemovePreprocessor.remove_cell_tags={\"hidden_cell\"}",
        "--output=tests/models_test")
    cmd.CombinedOutput()
    cmd := exec.Command("go", "test", "./tests")
    stdoutStderr, err := cmd.CombinedOutput()
    fmt.Printf("%s\n", stdoutStderr)
}

Test()


