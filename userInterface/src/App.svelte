<script>

import {dataBase} from "./lib/api.js"
const db = new dataBase;

let val;
let temp;

function search()
{
    temp = db.getTimeByName(val);
}


</script>

<h1>Time Tracker</h1>
<p>This application automatically tracks your usage time</p>
<p>Improve productivity greately</p>


<!-- {#await db.getAppNames()}
    <p>Loading data.....</p>
{:then value} 
    
    {#each value as v}

    <p>{v.appName} - {v.context}</p>
    {/each}

{/await} -->
    

<input bind:value={val}>
<button on:click={search}>Search</button>


{#await temp}
<p>Searching</p>    
{:then val}

    <p>{val}</p>
    
{/await}