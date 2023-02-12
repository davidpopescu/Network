function edit(id) {
  document.querySelector(`#editArea${id}`).style.display = 'block';
  document.querySelector(`#editButton${id}`).style.display = 'block';
  document.querySelector(`#editArea${id}`).innerHTML = document.querySelector(`#post-${id}`).innerHTML;
  document.querySelector(`#editButton${id}`).addEventListener('click', () => {
    fetch(`/edit/${id}`, {
      method: 'PUT',
      body: JSON.stringify({
        post: document.querySelector(`#editArea${id}`).value,
      }),
      headers: {
        'Content-Type': 'application/json',
      }
    });
        document.querySelector(`#editArea${id}`).style.display = 'none';
        document.querySelector(`#editButton${id}`).style.display = 'none';
        document.querySelector(`#post-${id}`).innerHTML = document.querySelector(`#editArea${id}`).value;
      
  });
}

function like (id) {
  button = document.querySelector(`#btn${id}`);
  likeButton = document.querySelector(`#likeButton${id}`);
  likedNumber = document.querySelector(`#likedNumber${id}`);
    if (button.style.backgroundColor == 'red'){
      button.style.backgroundColor = 'rgb(221, 221, 221)';
      fetch(`/like/${id}`, {
        method: 'POST',
        body: JSON.stringify({
          liked : false,
        })        
    })
    likedNumber.innerHTML = parseInt(likedNumber.innerHTML) - 1;    
    } else {
      button.style.backgroundColor = 'red';
      fetch(`/like/${id}`, {
        method: 'POST',
        body: JSON.stringify({
          liked : true,
        })
    })
      likedNumber.innerHTML = parseInt(likedNumber.innerHTML) + 1;
    }
}