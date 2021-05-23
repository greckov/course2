"use strict";

(function () {
  const postId = document.querySelector('[data-post-id]').dataset.postId;
  const modal = new bootstrap.Modal(document.getElementById('add-comment-modal'));
  const commentCreationForm = document.getElementById('comment-creation-form');
  const likePostButton = document.getElementById('like-btn');
  const dislikePostButton = document.getElementById('dislike-btn'); 
  const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
  let replyCommentId = null;

  // Function definitions
  async function sendUserReaction (button, reactionType) {
    const data = new FormData();
    data.set('csrfmiddlewaretoken', csrfToken);
    data.set('reaction', reactionType);

    const response = await fetch(`/post/${postId}/set_reaction/`, {
      method: 'POST',
      body: data
    });

    if (response.status === 201) {
      likePostButton.disabled = true;
      dislikePostButton.disabled = true;

      const countLabel = button.querySelector('.reaction-count');
      countLabel.innerText = +countLabel.innerText + 1;
    } else {
      alert('Failed to set post reaction');
    }
  }

  // Setup element event listeners
  for (const button of document.getElementsByClassName('reply-to-comment-btn')) {
    button.addEventListener('click', function () {
      replyCommentId = this.dataset.commentId;
      modal.show();
    });
  }

  document.getElementById('add-post-comment-btn').addEventListener('click', function () {
    replyCommentId = null;
    modal.show();
  });

  document.getElementById('perform-comment-creation-btn').addEventListener('click',  async () => {
    const requestData = new FormData(commentCreationForm);

    if (replyCommentId) {
      requestData.set('parent_id', replyCommentId);
    }

    const response = await fetch(`/post/${postId}/create_comment/`, {
      method: 'POST',
      body: requestData
    });

    if (response.status === 201) {
      location.reload();
    } else {
      alert('Виникла помилка під час створення коментару');
    }
  });

  likePostButton.addEventListener('click', async function () {
    await sendUserReaction(this, 'like');
  });

  dislikePostButton.addEventListener('click', async function () {
    await sendUserReaction(this, 'dislike');
  });
}());
