<script>
    import * as d3 from "d3";
    import { onMount } from "svelte";
    import {sortByKeyDesc} from "./logic"
    export let data;

const width = 150, height = 120, margin = 10;
const radius = Math.min(width, height) / 2 - margin
const color = d3.scaleOrdinal()
    .domain(["Productive","UnProductive","SemiProductive","UnCatogarized"])
    .range(["#57FF19", "#FF0800", "#FF5B0D", "#6b486b"])
const pie = d3.pie()
    .value((d) => {return d.time; })
const data_ready = pie(data)

sortByKeyDesc(data,"time").forEach(element => {
    let labels = [];
    labels.push(element.name)
});

onMount(async() =>{

const svg = d3.select("#my_dataviz")
    .append("svg")
        .attr("width", width)
        .attr("height", height)
    .append("g")
        .attr("transform", `translate(${width / 2},${height / 2})`)

svg
    .selectAll('g')
    .data(data_ready)
    .enter()
    .append('path')
    .attr('d',d3.arc()
    .innerRadius(30)
    .outerRadius(radius))
    .attr('fill', (d) => {
        return(color(d.data.name))})

const legend = d3.select("#legend")
    .append('svg')
    .attr("width", width+50)
    .attr("height", height)

legend
.selectAll()
    .data(data_ready)
    .enter()
    .append("text")
    .attr("x",(d,i) => i)
    .attr("y",(d,i) =>{
        const v = i+15+(30*data.findIndex((item, i) =>  item.name === d.data.name))
        return v;
    })
    .attr("fill",(d)=>{
        return (color(d.data.name))
    })
    .text((d) => d.data.name + " : " +Math.round(d.data.time/6)/10+" Mins")
})
</script>

<div id="my_dataviz">
</div>

<div id="legend"></div>