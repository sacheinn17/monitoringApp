<script>

    import { fade } from "svelte/transition";

    export let awaitVal;
    export let card = false;
    export let title = "";
    export let customClass = "w-72"
    $:cardClassAtr = card ? "card bg-base-200 shadow-inner hover:shadow-2xl transition-shadow ":"";
</script>

<div class = "p-0 grow-0 h-fit mx-2 {cardClassAtr} {customClass}" transition:fade>
<div class:card-body = {card} class = "card-body">
    <p class="card-title ">{title}</p>
    {#await awaitVal}   
    <p>Loading</p>    
    {:then response}
        <slot {response}/>
    {:catch someError}
    error while loading {someError}<br>
    {/await}
</div>
</div>
