

function submitted(){
    var playlistName = document.getElementById('playlist').value;
    var searchPhrase = document.getElementById('phrases').value;
    
    fetch('http://localhost:5000/getByTitle/' + searchPhrase + "/" + playlistName ).then(res => {
        return res.text();
    }).then(res => {
        // console.log(res);
        // window.location = res;
        let embedded = `<center>
        <pre>

        </pre>
        <embed src="${res}" width="600" height="600">
       
        </center>`;
       document.body.innerHTML+= embedded;
    });
    
}

function submitted2(){
    var playlistName = document.getElementById('playlist').value;
    var searchPhrase = document.getElementById('phrases').value;
    
    fetch('http://localhost:5000/getByLetter/' + searchPhrase + "/" + playlistName ).then(res => {
        return res.text();
    }).then(res => {
        // console.log(res);
        // window.location = res;
        let embedded = `<center>
        <pre>
        
        </pre>
        <embed src="${res}" width="600" height="600">
        
        </center>`;
       document.body.innerHTML+= embedded;
    });
    
}

// THIS IS 
// <!-- html button designing and calling the event in javascript -->
// <input id="btntest" type="button" value="Check" 
//        onclick="window.location.href = 'http://www.google.com'" />


// function createPlaylist(){
//     const songarray = ["1,", "4"];
//     let description = "This is ymsldn jfsbjkfhabiufbehwv jkhbk";
//     fetch('http://localhost:5000/createPlaylist/' + JSON.stringify(songarray) + description).then(res => {
//         return res.json();
//     }).then(res => {
//         // console.log(res);
//         alert(res);
//     })
// }