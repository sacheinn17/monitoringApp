<script>
import {dataBase} from "./lib/api.js"
import {getDate} from "./lib/utilities.js";
import DispData from "./lib/dispData.svelte";
import { onMount } from "svelte";
import {getTop5Apps} from "./lib/utilities.js";
import DonutChart from "./lib/donutChart.svelte"
import { fade } from "svelte/transition";
import LineChart from "./lib/lineChart.svelte";
import { displayCatogaries } from "./lib/stores/lists.js";
import { getDates } from "./lib/utilities.js";

const db = new dataBase;
let temp = [];
let totalTime ;
let top5Apps = [];
let t;
let today = new Date();
let date = '';
$:date = getDate(today); 

let firstDate = '';


$:{
    console.log(date,today);
    setFetches();
    firstDate = getDates(today)[0];
}

async function setFetches(){

    // @ts-ignore
    temp = db.getCatogariesAndTime(date);
    totalTime = await db.getTotalTime(date);
    // @ts-ignore
    top5Apps =await getTop5Apps(db.getAppUsage(date));
}

onMount(async() =>
{
 setFetches()       
})

async function refresDataBase(){
    t = await db.refreshDataBase()
};
</script>

<div class="flex justify-center">
    <img src="/src/assets/clock-tilted.svg" alt="" srcset="">
    <h1 class = "text-primary font-bold text-xl text-center">Hour Hand</h1>
</div>
    <p class="text-secondary text-center  text-ellipsis p-1">Track your activity around the clock</p>

<div class="flex flex-col" transition:fade>
    <div class="row1 flex justify-between">

        <DispData awaitVal = {totalTime} let:response>
            <p class = "text-info">Total Screen Time : {Math.round(response/6)/10} Minutes</p>
        </DispData>
        
        <div class="dateSection flex w-96 justify-evenly">
            <button class="btn btn-circle btn-outline btn-sm " on:click={() =>{today.setDate(today.getDate()-1);date = getDate(today);console.log(today)}}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left-short" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M12 8a.5.5 0 0 1-.5.5H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5H11.5a.5.5 0 0 1 .5.5z"/>
                  </svg>
              </button>
            <p class = "text-2xl text-accent hover:text-accent-focus">{date}</p>
            <button class="btn btn-circle btn-outline btn-sm " on:click={() =>{today.setDate(today.getDate()+1);date = getDate(today);console.log(today)}}>
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right-short" viewBox="0 0 16 16">
                    <path fill-rule="evenodd" d="M4 8a.5.5 0 0 1 .5-.5h5.793L8.146 5.354a.5.5 0 1 1 .708-.708l3 3a.5.5 0 0 1 0 .708l-3 3a.5.5 0 0 1-.708-.708L10.293 8.5H4.5A.5.5 0 0 1 4 8z"/>
                  </svg>
              </button>
        </div>

        <button class = "btn btn-outline flex-grow-0 btn-wide" on:click={refresDataBase}>Refresh Data Base</button>

    </div>
    <div class="row2 flex flex-row" transition:fade>
        <DispData card = {true} awaitVal = {temp} let:response title = "Usage time by Catogary" customClass = "w-2/6">
            <div class="flex">
                <DonutChart data={response}/>
            </div>
            
        </DispData>
        {#key firstDate}
        <LineChart db = {db} today = {date}/>
        {/key}
        
    </div> 
<div class="flex">

    <DispData card = {true} awaitVal = {top5Apps} let:response title = "Most Used Apps">
        {#each response as key}
        {key.name} : <progress class = "progress progress-primary" value = {Math.round(key.time/6)/10} max = {totalTime/60}></progress>
        {/each}
    </DispData>

    {#each $displayCatogaries as name }
        <DispData card ={true} awaitVal = {getTop5Apps(db.getNameByCat(name,date))} let:response>
            <div class="flex">
                <p class = "card-title">{name}</p>
                <button class= "btn" on:click={function() {$displayCatogaries.splice($displayCatogaries.indexOf(name),1);$displayCatogaries = [...$displayCatogaries];console.log($displayCatogaries)}}>
                    <svg height="16" width="16" version="1.1" id="Capa_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 26 26" xml:space="preserve"><g><path style="fill:red;" d="M21.125,0H4.875C2.182,0,0,2.182,0,4.875v16.25C0,23.818,2.182,26,4.875,26h16.25 C23.818,26,26,23.818,26,21.125V4.875C26,2.182,23.818,0,21.125,0z M18.78,17.394l-1.388,1.387c-0.254,0.255-0.67,0.255-0.924,0 L13,15.313L9.533,18.78c-0.255,0.255-0.67,0.255-0.925-0.002L7.22,17.394c-0.253-0.256-0.253-0.669,0-0.926l3.468-3.467 L7.221,9.534c-0.254-0.256-0.254-0.672,0-0.925l1.388-1.388c0.255-0.257,0.671-0.257,0.925,0L13,10.689l3.468-3.468 c0.255-0.257,0.671-0.257,0.924,0l1.388,1.386c0.254,0.255,0.254,0.671,0.001,0.927l-3.468,3.467l3.468,3.467 C19.033,16.725,19.033,17.138,18.78,17.394z"/></g></svg>
                </button>
            </div>
                {#each response as key }
                    {key.name} : <progress class = "progress progress-primary" value = {Math.round(key.time/6)/10} max = {totalTime/60}></progress>
                {/each}
            </DispData>
    {/each}

</div>
</div>