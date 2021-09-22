block_events('btn')


function block_events(id){
        let btn = document.getElementById(id)
        btn.addEventListener('click', function(event){
        event.preventDefault()
    })
}



function go_to_chat(msg){
    var conteiner = document.getElementsByClassName('conteiner')[0]
    document.getElementsById('login').style.display = 'none';
    
    if (screen.width < 600){
        conteiner.style.display = 'block';
        alert('block')
    } else {
        conteiner.style.display = 'flex'
        alert('flex')
    }
    
    var tag = document.createElement('p');
    var text = document.createTextNode(msg);
    tag.appendChild(text);
    document.getElementById('chat').appendChild(tag)
}


