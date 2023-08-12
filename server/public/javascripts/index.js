const img = document.querySelector('img');

const init = async () => {
    const res = await fetch('/api/media/image/e654e57852b1a1a5a2f3042c24f3ac4a');
    console.log(res)
}

init();