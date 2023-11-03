<script>
    export let usage;
    export let loadText = "Loading ";
    export let awaitVal;
</script>


{#await awaitVal}
<p>{loadText} {usage}</p>    
{:then val}
    {val}
{:catch someError}
    error while loading {usage} : {someError.message}<br>
{/await}
