<script>

    import { fade } from "svelte/transition";

    export let awaitVal;
    export let card = false;
    export let title = "";
    $:cardClassAtr = card ? "card bg-base-200 shadow-inner hover:shadow-2xl transition-shadow ":"";
</script>

<div class = "p-0 grow-0 w-fit h-fit mx-2 {cardClassAtr}" transition:fade>
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
