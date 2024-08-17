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
  [Moonlight Moo Juice 1gal], [\$34.56],
  [Curved Yellow Happiness], [\$12.94],
  [Soap Bubbles in a Box 42ct], [\$524.01],
  [Yeasty Rectangle of Joy 20oz], [\$0.17],
  [Hen Fruit Carton Large 18ct], [\$1455.99],
  [Clucky Slices], [\$8.11],
  [], [],

  table.hline(),

  [Subtotal], [],
  [Tax (6.5%)], [],
  [], [],

  table.hline(),

  [*TOTAL*], [],
  [], [],

  table.hline(),

  [VISA], [],
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
