<script>
import * as d3 from "d3";
import {onMount} from "svelte";
import {getTimeCat} from "./utilities";
import {getDates} from "./utilities";
export let db;
export let today;

onMount(() =>{
db.getCatNames().then(res =>{
    let svg = d3.select("#lineChart");
    let dates = getDates(today);
    let catogaries = res[0].catogaries;
    console.log(catogaries);
    const pxX = 850;
    const pxY = 250;
    svg.attr("width",pxX);
    svg.attr("height",pxY);
    var scX = d3.scalePoint().domain(dates).range([35,pxX-50]);
    var scY = d3.scaleLinear().domain([350,0]).range([20,pxY-50]);   
    const color = d3.scaleOrdinal().domain(["Productive","UnProductive","SemiProductive","UnCatogarized"]).range(["#57FF19", "#FF0800", "#FF5B0D", "#6b486b"])

    catogaries.forEach(cat => {
    let nodes = []
    dates.forEach((date) => {
        var time = getTimeCat(date,cat)
        time.then(time =>{
            if (time!=undefined){
                svg.append('g').selectAll('circle').data(d => [d]).enter()
                    .append('circle').attr("r",6)
                    .attr('cx',() => scX(date))
                    .attr('cy', () =>  scY(time))
                    .attr('fill', ()=> color(cat))
                nodes[dates.indexOf(date)] = [scX(date),scY(time)]
            }

            if (!(nodes.length <7)){           
            for (let i = 0; i < nodes.length-1; i++){
            try{
                svg
                    .append('line')
                    .attr("x1", () => nodes[i][0])
                    .attr("y1", () => nodes[i][1])
                    .attr("x2", () => nodes[i+1][0])
                    .attr("y2", () => nodes[i+1][1] )
                    .style('stroke',() => color(cat))
                    .attr("stroke-width",3)
            }
            catch(e){
                console.log(e);
                continue;
            }
            }                    
            }
        })
    })
})         

    var ay = d3.axisBottom(scX);
    var ax = d3.axisLeft(scY);
    svg.append('g')
        .attr("transform", "translate("+0+", " + (pxY-50)  +")")
        .call(ay);

    svg.append('g')
        .attr("transform", "translate("+30+", " +0  +")")
        .call(ax)
})
})
</script>

<svg id = "lineChart" class = "mx-8" >

</svg>
