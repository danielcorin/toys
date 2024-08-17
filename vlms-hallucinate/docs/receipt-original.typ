#set page(width: 3.15in, height: auto, margin: 0.2in)
#set text(font: "Courier", size: 9pt)

#table(
  columns: (1fr, auto),
  inset: 2pt,
  align: (x, y) => if x == 0 { left } else { right },
  stroke: none,

  table.header(
    [*WALMART*],
    [*RECEIPT*]
  ),

  [2700 S Kirkman Rd],
  [08/15/2024],
  [Orlando, FL 32811],
  [],
  [Store: 2591  Register: 007],
  [Cashier: JOHN],
  [Trans \#: 7829-5463-9102-8374],
  [],

  table.hline(),

  [Item], [Price],
  [Great Value Milk 1gal], [\$3.27],
  [Bananas 2.35 lb \@ \$0.58/lb], [\$1.36],
  [Tide Pods 42ct], [\$12.97],
  [Bread Wheat 20oz], [\$1.88],
  [Eggs Large 18ct], [\$4.23],
  [Chicken Breast 2.73lb \@ \$2.97/lb], [\$8.11],
  [], [],

  table.hline(),

  [Subtotal], [\$31.82],
  [Tax (6.5%)], [\$2.07],
  [], [],

  table.hline(),

  [*TOTAL*], [*\$33.89*],
  [], [],

  table.hline(),

  [VISA], [\$33.89],
  [xxxxxxxxxxxx5678], [],
  [Approval: 637294], [],
  [], [],

  table.hline(),

  [Items Sold 6], [],
  [TC\# 2735 9826 4019 3728 5647], [],
  [], [],
  [Thank you for shopping at Walmart!], [],
  [Save even more with Walmart+], [],
  [www.walmart.com/plus], [],
  [], [],
)
