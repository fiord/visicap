const width = window.innerWidth;
const height = window.innerHeight;
const svg = d3.select("svg")
  .attr("viewBox", [0, 0, width, height]);
const color = (v) => {
  return d3.schemeCategory10[v % d3.schemeCategory10.length];
};

const select = document.querySelector("#fileSelector");
const options = document.querySelectorAll("#fileSelector option");

const drag = (simulation) => {
  const dragStarted = (d) => {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x;
    d.fy = d.y;
  };

  const dragged = (d) => {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
  };

  const dragended = (d) => {
    if (!d3.event.active) simulation.alphaTarget(0);
    d.fx = null;
    d.fy = null;
  };

  return d3.drag()
    .on("start", dragStarted)
    .on("drag", dragged)
    .on("end", dragended);
};

select.addEventListener("change", async () => {
  let idx = select.selectedIndex;
  if (idx === 0)  return;
  const res = await fetch("/api/data/" + options[idx].innerHTML);
  console.log(res);
  const data = await res.json();
  // container内部になんか作る
  const title = Object.keys(data)[0];
  const links = data[title].dist.map((v, i) => v.map((d, j) => {
    return {
      source: i,
      target: j,
      value: d
    };
  })).reduce((a, c) => {
    return a.concat(c);
  });
  const nodes = data[title].ele.map((v, i) => {
    return {
      id: i,
      text: v.data,
      group: v.label,
      time: v.time
    };
  });
  console.log(nodes);
  console.log("links/nodes: ok");
  const sim = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(d => d.id))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));
  console.log("sim: ok");
  const link = svg.append("g")
    .attr("stroke", "#999")
    .attr("stroke-opacity", 0.0)
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
    .attr("stroke-width", d => Math.sqrt(d.value));
  const node = svg.append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("r", 5)
    .attr("fill", (v) => color(v.group))
    .call(drag(sim));
  console.log("link: ok");

  node.append("title")
    .text(d => d.time + ":" + d.text);
  console.log("title: ok");

  sim.on("tick", () => {
    link.attr("x1", d => d.source.x)
      .attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x)
      .attr("y2", d => d.target.y);

    node.attr("cx", d => d.x)
      .attr("cy", d => d.y);
  });
  console.log("tick: ok");
});
