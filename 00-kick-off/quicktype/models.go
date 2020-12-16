package main

type Sku string

type Integer float64

type Batch struct {
	Allocations []OrderLine `json:"allocations"`
	Qty         int64       `json:"qty"`        
	Reference   string      `json:"reference"`  
	Sku         string      `json:"sku"`        // TypeScript-JSON Schema for quicktype code generation.
}

type OrderLine struct {
	ID  string `json:"id"` 
	Qty int64  `json:"qty"`
	Sku string `json:"sku"`// TypeScript-JSON Schema for quicktype code generation.
}

type Order struct {
	OrderLines []OrderLine `json:"orderLines,omitempty"`
	Reference  string      `json:"reference"`           
}
