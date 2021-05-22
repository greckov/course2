"use strict";

(function () {
  const postId = document.querySelector('[data-post-id]').dataset.postId;
  const modal = new bootstrap.Modal(document.getElementById('add-comment-modal'));
  const commentCreationForm = document.getElementById('comment-creation-form');
  let replyCommentId = null;

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
}());
