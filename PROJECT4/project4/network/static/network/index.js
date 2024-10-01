// Function to get the CSRF token from cookies
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

// Function to handle the submit of an edit form
function submitHandler(post_id) {
  const textareaValue = document.getElementById(`textarea_${post_id}`).value;
  const contentElement = document.getElementById(`content_${post_id}`);
  const modalElement = document.getElementById(`model_edit_post_${post_id}`);

  fetch(`/edit/${post_id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken")
    },
    body: JSON.stringify({
      content: textareaValue
    })
  })
  .then(response => response.json())
  .then(result => {
    if (result && result.data) {
      // Update the content in the post after editing
      contentElement.innerHTML = result.data;

      // Close the modal programmatically using Bootstrap modal method
      $(`#model_edit_post_${post_id}`).modal('hide');
    } else {
      console.error("Error in response:", result);
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });
}
