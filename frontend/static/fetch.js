export async function fetchData() {
    const lists = [];
    try {
     
        const response = await fetch('/get_results'); // Adjust the URL as necessary

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        data.forEach(item => {
            let ds = {
                subjSumm: item.subjSummary,
                objSumm: item.objSummary,
                subj: item.subj,
                rel: item.rel,
                obj: item.obj
            }
            lists.push(ds)
        });
        return lists
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

document.getElementById('fetchButton').addEventListener('click', fetchData);