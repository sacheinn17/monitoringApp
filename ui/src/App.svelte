<script>

// import "../src/app.css"
import {dataBase} from "./lib/api.js";
import DispData from "./lib/dispData.svelte";
import { onMount } from "svelte";
const db = new dataBase;
let temp = db.getTimeByCatogary("today");
let totalTime;


onMount(async() =>
{
    totalTime = db.getTotalTime();
    // temp = db.getTimeByCatogary("today");
})

</script>

<h1 class = " text-cyan-800 text-center">Time Tracker</h1>
<p class="text-green-500 text-center">This application automatically tracks your usage time and Improve productivity greately</p>


<div class = "card ">
    <div class="card-body">
{#await temp}   
<p>Loading</p>    
{:then val}
{#each val as key}
{key.catogary} : {key.time} <br>
{/each}
{:catch someError}
error while loading {someError}<br>
{/await}

</div>
</div>
{#await totalTime}   
<p>Loading</p>    
{:then val}
    Total Usage time is {val}
{:catch someError}
error while loading {someError}<br>``
{/await}