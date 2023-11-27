<script>
    export let awaitVal;
    export let card = false;
    export let title = "";
    $:cardClassAtr = card ? "card bg-base-200 shadow-inner hover:shadow-2xl transition-shadow ":"";
</script>

<div class = "p-1 grow-0 w-fit h-fit m-1{cardClassAtr} ">
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
