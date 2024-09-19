document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // Submit Composed Email
  document.querySelector('#compose-form').addEventListener('submit', send_email);
  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

}

function load_reply(email){
  
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = email.sender;
  let reply_subject = "";
  if (email.subject.includes("Re :")) {
    reply_subject = email.subject;
  } else {
    reply_subject = `Re : ${email.subject}`;
  }

  document.querySelector('#compose-subject').value = `${reply_subject}`;
  document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote : ${email.body}`;

}


function show_email(email_id){
  
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'block';
  // Select the parent element (email-content-view)
  const emailContentView = document.querySelector('#email-content-view');

  // Clear previous content by setting innerHTML to an empty string
  emailContentView.innerHTML = '';
    fetch(`/emails/${email_id}`)
    .then(response => response.json())
    .then(email => {

        // ... do something else with email ...
        const email_element = document.createElement('div');
        email_element.className = "list-group-item";
        email_element.innerHTML = `
        <h5>Sender:${email.sender}</h5>
        <h5>Recipients:${email.recipients}</h5>
        <h6>Subject:${email.subject}</h6>
        <h7>Body:${email.body}</h7>
        <p>${email.timestamp}</p>
        <div><button id="reply">Reply</button></div>
        `;
        emailContentView.append(email_element);
        // Reply from Current Email
        document.querySelector('#reply').addEventListener('click', () => load_reply(email));

         // Mark as Read
      if (!email.read){
        fetch(`/emails/${email_id}`, {
          method: 'PUT',
          body: JSON.stringify({
              read: true
          })
        })
      }
    });
}


function archive_email(email_id, archive_state) {
  fetch(`/emails/${email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: archive_state  // Directly send the archive state as true or false
      })
  }).then(() => {
      console.log(`Email ${archive_state ? "archived" : "unarchived"} successfully!`);
      // Now reload the mailbox after the state change is confirmed
      load_mailbox('inbox');
  }).catch(error => {
      console.error('Error:', error);
  });
}



function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-content-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  
  // Get mail list
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);
      
      // Loop through all emails
      emails.forEach(element => {
        
        // Create box for each email
        const email_element = document.createElement('div');
        email_element.className = element.read ? "read" : "unread";
        email_element.classList.add("list-group-item");
        
        // Create a unique button ID using email id
        const buttonId = `archive-btn-${element.id}`;
        
        // Set the button text based on the archived status
        const buttonText = element.archived ? "Unarchive" : "Archive";
        
        email_element.innerHTML = `
          <h5>Sender: ${element.sender}</h5>
          <h6>Subject: ${element.subject}</h6>
          <p>${element.timestamp}</p>
          ${mailbox !== "sent" ? `<div><button id="${buttonId}">${buttonText}</button></div>` : ""}
        `;
        
        // Append the email element to the view
        document.querySelector('#emails-view').append(email_element);

        // Move to show email when clicking the email element
        email_element.addEventListener('click', function() {
          show_email(element.id);
        });

        // Only add archive/unarchive functionality if not in the "sent" mailbox
        if (mailbox !== "sent") {
          document.getElementById(buttonId).addEventListener('click', (event) => {
            // Stop the click event from propagating to the email element
            event.stopPropagation();
        
            // Call archive_email with email ID and toggle archived status
            archive_email(element.id, !element.archived);
        
            // Remove the email element from the DOM after archiving/unarchiving
            email_element.remove();
          });
        }
      });
  });
}

function send_email(event){
  event.preventDefault();
  
  //Save the form value
  const recipients = document.querySelector('#compose-recipients').value ;
  const subject =document.querySelector('#compose-subject').value ;
  const body =document.querySelector('#compose-body').value;

  //Send the email
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
      load_mailbox('sent')
  });
  

}