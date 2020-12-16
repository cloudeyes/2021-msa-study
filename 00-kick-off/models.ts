/** 
 * TypeScript-JSON Schema for quicktype code generation.
 */

type SKU = string;
type integer = number;

class Batch {
    reference: string;
    sku: SKU;
    qty: integer;
    allocations: OrderLine[] = [];
}

class Order {
    reference: string;
    orderLines?: OrderLine[];
}

class OrderLine {
    id: string;
    sku: SKU;
    qty: integer;
}
