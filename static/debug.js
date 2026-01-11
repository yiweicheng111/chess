function wait(ms){
    return new Promise(res=>{setTimeout(res,10)});
}
self.addEventListener('message', async (e)=>{
    while (true){
        await wait(10);
        console.log(window.selected);
        console.log(window.selectedSqr);
    }
});