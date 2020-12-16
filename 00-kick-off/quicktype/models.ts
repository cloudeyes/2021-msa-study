type integer = number;

export class Batch {
    reference: string;
    sku: string;
    qty: integer;
    allocations: OrderLine[] = [];
}

export class Order {
    reference: string;
    orderLines: OrderLine[] = [];
}

export class OrderLine {
    id: string;
    sku: string;
    qty: integer;
}
