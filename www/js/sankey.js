// code for this was inspired by; https://observablehq.com/@mbostock/flow-o-matic, https://observablehq.com/@jasper/005-sankey-graph

const data = {
    nodes: [
        {name: "Brick Kilns", type: "sector"},
        {name: "Domestic", type: "sector"}, 
        {name: "Industries", type: "sector"}, 
        {name: "Power Generation", type: "sector"}, 
        {name: "Transport", type: "sector"}, 
        {name: "Coal", type: "source"}, 
        {name: "Waste", type: "source"}, 
        {name: "Kerosene", type: "source"}, 
        {name: "Fuelwood & other", type: "source"}, 
        {name: "Biomass", type: "source"}, 
        {name: "High Speed Diesel", type:"source"}, 
        {name: "LPG", type: "source"}, 
        {name: "Natural Gas", type: "source"}, 
        {name: "Residual Fuel Oil", type: "source"}, 
        {name: "Fossil Fuel", type: "source"}, 
        {name: "Rickshaws", type: "source"}, 
        {name: "Large Cars", type: "source"}, 
        {name: "Small Trucks/Pickups", type: "source"}, 
        {name: "Large Trucks", type: "source"}, 
        {name: "Tractors", type: "source"}, 
        {name: "SUVs/Jeeps", type: "source"}, 
        {name: "Wagons", type: "source"}, 
        {name: "Motorbikes", type: "source"}, 
        {name: "Small Cars", type: "source"}, 
        {name: "Buses", type: "source"},
        {name: "CO", type: "pollutant"}, 
        {name: "NOx", type: "pollutant"}, 
        {name: "PM2.5", type: "pollutant"}, 
        {name: "SOx", type: "pollutant"}


    ], 
    links : [
        // sector --> source
        {source: "Brick Kilns", target: "Coal", value: 17.316300000000002 }, 
        {source: "Domestic", target: "Waste", value: 9.109300000000001}, 
        {source: "Domestic", target: "Kerosene", value: 0.01361}, 
        {source: "Domestic", target: "LPG", value: 0.1618}, 
        {source: "Domestic", target: "Fuelwood & other", value: 12.7855}, 
        {source: "Domestic", target: "Coal", value: 0.0091}, 
        {source: "Domestic", target: "Natural Gas", value: 2.3167999999999997}, 
        {source: "Industries", target: "Biomass", value: 0.5295}, 
        {source: "Industries", target:"High Speed Diesel", value: 2.4214}, 
        {source: "Industries", target: "LPG", value: 0.2942},
        {source: "Industries", target: "Coal", value: 8.518}, 
        {source: "Industries", target: "Natural Gas", value: 1.8929999999999998}, 
        {source: "Industries", target: "Residual Fuel Oil", value: 0.5699}, 
        {source: "Power Generation", target: "Fossil Fuel", value: 18.8128}, 
        {source: "Transport", target: "Rickshaws", value: 37.1227}, 
        {source: "Transport", target: "Large Cars", value: 13.6671},
        {source: "Transport", target: "Small Trucks/Pickups", value: 5.5867},
        {source: "Transport", target: "Large Trucks", value: 22.235200000000003},
        {source: "Transport", target: "Tractors", value: 0.3965},
        {source: "Transport", target: "SUVs/Jeeps", value: 9.1881},
        {source: "Transport", target: "Wagons", value: 5.5764000000000005},
        {source: "Transport", target: "Motorbikes", value: 94.5336},
        {source: "Transport", target: "Small Cars", value: 8.3978},
        {source: "Transport", target: "Buses", value: 20.167},

        // source --> pollutant
        {source: "Motorbikes", target: "CO", value: 91.9247}, 
        {source: "Rickshaws", target: "CO", value: 35.7167},
        {source: "Fossil Fuel", target: "SOx", value: 15.876499999999998},
        {source: "Large Trucks", target: "NOx", value: 13.1879},
        {source: "Coal", target: "CO", value: 13.6476},
        {source: "Buses", target: "NOx", value: 12.4709},
        {source: "Fuelwood & other", target: "CO", value: 11.5929},
        {source: "Large Cars", target: "CO", value: 11.1308},
        {source: "Large Trucks", target: "CO", value: 8.5214},
        {source: "Waste", target: "CO", value: 7.5086}, 
        {source: "Buses", target: "CO", value: 7.2523},
        {source: "Small Cars", target: "CO", value: 7.1357},
        {source: "SUVs/Jeeps", target: "NOx", value: 5.7061},
        {source: "Coal", target: "PM2.5", value: 11.2983}, 
        {source: "Wagons", target: "CO", value: 2.9138}, 
        {source: "Small Trucks/Pickups", target: "CO", value: 2.9138}, 
        {source: "SUVs/Jeeps", target: "CO", value: 2.7951},
        {source: "Fossil Fuel", target: "NOx", value: 2.6136999999999997},
        {source: "Motorbikes", target: "NOx", value: 2.2751},
        {source: "Small Trucks/Pickups", target: "NOx", value: 2.1678}, 
        {source: "Wagons", target: "NOx", value: 2.1678}, 
        {source: "Large Cars", target: "NOx", value: 2.1657},
        {source: "High Speed Diesel", target: "NOx", value: 1.7662},
        {source: "Waste", target: "PM2.5", value: 1.5632},
        {source: "Natural Gas", target: "NOx", value: 2.3979999999999997},
        {source: "Rickshaws", target: "NOx", value: 1.3141},
        {source: "Fuelwood & other", target: "PM2.5", value: 1.1926},
        {source: "Small Cars", target: "NOx", value: 0.9971},
        {source: "Natural Gas", target: "CO", value: 1.7530999999999999},
        {source: "SUVs/Jeeps", target: "PM2.5", value: 0.6869},
        {source: "High Speed Diesel", target: "CO", value: 0.533},
        {source: "Large Trucks", target: "PM2.5", value: 0.5259},
        {source: "Small Trucks/Pickups", target: "PM2.5", value: 0.5051},
        {source: "Wagons", target: "PM2.5", value: 0.4948},
        {source: "Buses", target: "PM2.5", value: 0.4438},
        {source: "Large Cars", target: "PM2.5", value: 0.37060000000000004},
        {source: "Motorbikes", target: "PM2.5", value: 0.3338},
        {source: "Coal", target: "NOx", value: 0.8975},
        {source: "Residual Fuel Oil", target: "NOx", value: 0.2966},
        {source: "Tractors", target: "NOx", value: 0.277},
        {source: "Small Cars", target: "PM2.5", value: 0.265},
        {source: "Biomass", target: "NOx", value: 0.2588},
        {source: "Fossil Fuel", target: "CO", value: 0.2407},
        {source: "Biomass", target: "CO", value: 0.2389},
        {source: "Residual Fuel Oil", target: "CO", value: 0.2326},
        {source: "LPG", target: "NOx", value: 0.2532},
        {source: "LPG", target: "CO", value: 0.1829},
        {source: "High Speed Diesel", target: "PM2.5", value: 0.1222},
        {source: "Rickshaws", target: "PM2.5", value: 0.0919},
        {source: "Fossil Fuel", target: "PM2.5", value: 0.0819},
        {source: "Tractors", target: "CO", value: 0.0803},
        {source: "Residual Fuel Oil", target: "PM2.5", value: 0.0407},
        {source: "Tractors", target: "PM2.5", value: 0.0392},
        {source: "Waste", target: "NOx", value: 0.0375},
        {source: "Biomass", target: "PM2.5", value: 0.0318},
        {source: "Kerosene", target: "PM2.5", value: 0.012},
        {source: "LPG", target: "PM2.5", value: 0.0199},
        {source: "Kerosene", target: "NOx", value: 0.00001},
        {source: "Kerosene", target: "CO", value: 0.0016},
        {source: "Natural Gas", target: "PM2.5", value: 0.0587},
    ]
}
const svg = d3.select("#sankey");
const width = +svg.attr("width");
const height = +svg.attr("height");

const colorScale = d3.scaleOrdinal().domain(["sector", "source", "pollutant"]).range(["#FF6501", "#1181C8 ", "#B40028"]); 

// initializing the sankey function we will run our data on
const sankeyFunc = d3.sankey()
.nodeId(d => d.name)
.nodeWidth(15)
.nodePadding(12)
.extent([[160, 40], [width - 160, height - 40]]);


// passing our data through our sankey funtion
// creating copies of our nodes and links
const graph = sankeyFunc({
  nodes: data.nodes.map(d => ({ ...d })),
  links: data.links.map(d => ({ ...d }))
});

// Draw links
const links = svg.append("g")
  .attr("fill", "none")
  .attr("stroke-opacity", 0.4)
  .selectAll("path")
  .data(graph.links)
  .join("path")
    .attr("d", d3.sankeyLinkHorizontal())
    .attr("stroke", "#999")
    .attr("stroke-width", d => Math.max(1, d.width))
    .style("pointer-events", "stroke");

// custom tooltip
// Asked ChatGPT to help me set up the hover tool tip
const tooltip = d3.select("#tooltip");

links
.on("mouseover", function(d) {
// highlight the hovered link
d3.select(this)
  .attr("stroke-opacity", 0.8)
  .attr("stroke", "#cadb5c");

tooltip
  .style("opacity", 1)
  .html(
    `${d.source.name} → ${d.target.name}<br>` +
    `Value: ${d3.format(".3f")(d.value)} Kt`
  );
})
.on("mousemove", function(d) {
tooltip
  .style("left", (d3.event.pageX + 10) + "px")
  .style("top", (d3.event.pageY + 10) + "px");
})
.on("mouseout", function(d) {
d3.select(this)
  .attr("stroke-opacity", 0.4)
  .attr("stroke", "#999");

tooltip.style("opacity", 0);
});

// Draw nodes
// sankeyFunc calculates positions for every node and link
// here we are using those attributes to actually draw out the graph
const nodes = svg.append("g")
.append("g")
.selectAll("rect")
.data(graph.nodes)
.join("rect")
.attr("x", (d) => d.x0)
.attr("y", (d) => d.y0)
.attr("fill", (d) => colorScale(d.type))
.attr("height", (d) => d.y1 - d.y0)
.attr("width", (d) => d.x1 - d.x0);


// depth captures whether it is the left most or right most node
const maxDepth = d3.max(graph.nodes, d => d.depth);

const labelNames = svg.append("g")
.selectAll("text")
.data(graph.nodes)
.join("text")
.text(d => d.name)
.attr("class", d => `node-label depth-${d.depth}`)
.attr("x", d =>  d.depth === maxDepth ? d.x1 + 20 : d.x0 - 50)
.attr("y", d => (d.y0 + d.y1) / 2)
.attr("dy", "0.35em")
.attr("text-anchor", "middle")
.attr("dominant-baseline", "middle")
.attr("fill","black")
.attr("font-family", '"Source Sans Pro", Helvetica, sans-serif')
.attr("font-weight", 400)
.attr("font-size", "12px");


