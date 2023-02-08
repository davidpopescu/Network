function edit(id) {
  document.querySelector(`#editArea${id}`).style.display = 'block';
  document.querySelector(`#editButton${id}`).style.display = 'block';

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
  let liked = false;
  button = document.querySelector(`#btn${id}`);
  likeButton = document.querySelector(`#likeButton${id}`);
  button.style.backGroundColor = 'white';
  likedNumber = document.querySelector(`#likedNumber${id}`);
  likeButton.addEventListener('click', () => {
    if (button.style.backgroundColor == 'white') {
      likedNumber.innerHTML = parseInt(likedNumber.innerHTML) - 1;
      button.style.backgroundColor = 'red';
      fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          liked : true,
        })
    })
    } else {
      button.style.backgroundColor = 'white';
      likedNumber.innerHTML = parseInt(likedNumber.innerHTML) + 1, "Like";
      fetch(`/like/${id}`, {
        method: 'PUT',
        body: JSON.stringify({
          liked : false,
        })
    })
  }
  });
}