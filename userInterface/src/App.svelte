<script>

import {dataBase} from "./lib/api.js"
import DispData from "./dispData.svelte";
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

<h1>Time Tracker</h1>
<p>This application automatically tracks your usage time</p>
<p>Improve productivity greately</p>

{#await temp}   
<p>Loading</p>    
{:then val}
    {#each val as key}
        {key.catogary} : {key.time} <br>
    {/each}
{:catch someError}
    error while loading {someError}<br>
{/await}


{#await totalTime}   
<p>Loading</p>    
{:then val}
    Total Usage time is {val}
{:catch someError}
    error while loading {someError}<br>
{/await}


