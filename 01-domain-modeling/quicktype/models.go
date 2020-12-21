package main

type Integer float64

type Batch struct {
	Reference   string      `json:"reference"`  
	Sku         string      `json:"sku"`        
	Qty         int64       `json:"qty"`        
	Allocations []OrderLine `json:"allocations"`
}

type OrderLine struct {
	ID  string `json:"id"` 
	Sku string `json:"sku"`
	Qty int64  `json:"qty"`
}

type Order struct {
	Reference  string      `json:"reference"` 
	OrderLines []OrderLine `json:"orderLines"`
}
