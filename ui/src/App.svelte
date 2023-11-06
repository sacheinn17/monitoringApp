<script>

import {dataBase} from "./lib/api.js";
import DispData from "./lib/dispData.svelte";
import { onMount } from "svelte";
import {getTop5Apps} from "./lib/logic.js";
import DonutChart from "./lib/donutChart.svelte"
import { fade } from "svelte/transition";

const db = new dataBase;
let temp = [];
let totalTime = 0;
let top5Apps = [] ;
let t;
let today = new Date();
let date = '';

function getDate(today){
return today.getFullYear() + '-' + String(today.getMonth() + 1).padStart(2, '0') + '-' + String(today.getDate()).padStart(2, '0');}

$:date = getDate(today); 

$:{
    console.log(date);
    setFetches();
}

async function setFetches(){

    // @ts-ignore
    temp = db.getCatogariesAndTime(date);
    totalTime = await db.getTotalTime(date);
    // @ts-ignore
    top5Apps = getTop5Apps(db,date);
}

onMount(async() =>
{
 setFetches()   
})

async function refresDataBase(){
    t = await db.refreshDataBase()
};

</script>

<h1 class = " text-cyan-800 text-center">Time Tracker</h1>
<p class="text-green-500 text-center">This application automatically tracks your usage time and Improve productivity greately</p>

<div class="flex flex-col" transition:fade>
    <div class="col1 flex justify-between">

        <DispData awaitVal = {totalTime} let:response>
            Total Usage Time is {Math.round(response/6)/10} Minutes
        </DispData>
        
        <div class="dateSection flex w-96 justify-evenly">
            <button class="btn btn-circle btn-outline btn-sm " on:click={() =>{today.setDate(today.getDate()-1);date = getDate(today);console.log(today)}}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left-short" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5z"/>
                  </svg>
              </button>
            <p class = "text-2xl">{date}</p>
            <button class="btn btn-circle btn-outline btn-sm " on:click={() =>{today.setDate(today.getDate()+1);date = getDate(today);console.log(today)}}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right-short" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M4 8a.5.5 0 0 1 .5-.5h5.793L8.146 5.354a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 8.5H4.5A.5.5 0 0 1 4 8z"/>
                  </svg>
              </button>
        </div>

        <button class = "btn btn-outline flex-grow-0 btn-wide" on:click={refresDataBase}>Refresh Data Base</button>

    </div>

    <div class="col2 flex flex-row pb-3" transition:fade>
    <DispData card = {true} awaitVal = {temp} let:response title = "Usage time by Catogary">
        <div class="flex">

            <DonutChart data={response} />
        </div>
    </DispData>
    <div class="graph p-4">
        This is a graph
    </div>
    </div>

    <DispData card = {true} awaitVal = {top5Apps} let:response title = "Most Used Apps">
        {#each response as key}
        {key.name} : <progress class = "progress progress-primary" value = {Math.round(key.time/6)/10} max = {totalTime/60}></progress>
        {/each}
    </DispData>
</div>