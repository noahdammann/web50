document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');

  // Listen for email submission
  document.querySelector('#compose-form').addEventListener('submit', sendEmail);
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#single-email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // Get the appropriate mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {

    // Loop over the emails in the array
    emails.forEach(e => {
      const email_div = document.createElement('div');
      email_div.className = 'mailbox_div';
      email_div.id = e.read ? 'read' : 'unread';
      email_div.innerHTML = `
        <h1 class="mailbox_subject">${e.subject}</h1>
        <h2 class="mailbox_parties"><strong>To:</strong> ${e.recipients}</h2>
        <h2 class="mailbox_parties"><strong>From:</strong> ${e.sender}</h2>
        <h3 class="mailbox_timestamp"><i>${e.timestamp}</i></h3>
        <h4 class="mailbox_body">${e.body}</h4>
      `;

      // Add click functionality
      email_div.addEventListener('click', () => {
        viewEmail(e.id);
      })
      document.querySelector('#emails-view').append(email_div);
    })
  })
}

function sendEmail(event) {
  event.preventDefault();

  // Get user input
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  // Store email in backend
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: recipients,
      subject: subject,
      body: body,
    })
  })
  .then(() => {load_mailbox('sent')});
}

function viewEmail(id) {

  // Show the email and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#single-email-view').style.display = 'block';

  // Set inner HTML to empty
  document.querySelector('#single-email-view').innerHTML = '';
  
  // Fetch email details from backend
  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {
    
    // Change read status to true
    if (!email.read) {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          read: true
        })
      })
    }

    // Load content to HTML
    const email_view = document.createElement('div');
    email_view.className = 'email_view';
    email_view.innerHTML = `
      <h1 id="subject">${email.subject}</h1>
      <h2 id="parties">To: ${email.recipients}</h2>
      <h2 id="parties">From: ${email.sender}</h2>
      <pre><h3 id="body">${email.body}</h3></pre>
      <h4 id="timestamp"><i>${email.timestamp}</i></h4>
    `;
    document.querySelector('#single-email-view').append(email_view);

    // Archive functionality
    const archive_button = document.createElement('button');
    archive_button.className = 'function_button';
    archive_button.innerHTML = email.archived ? 'Unarchive' : 'Archive';
    archive_button.addEventListener('click', () => {
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          archived: !email.archived
        })
      })
      .then(() => {load_mailbox('archive')})
    });
    document.querySelector('#single-email-view').append(archive_button);

    // Reply functionality
    const reply_button = document.createElement('button');
    reply_button.innerHTML = 'Reply';
    reply_button.className = 'function_button';
    reply_button.addEventListener('click', () => {

      compose_email();

      // Check if RE: already present
      let subject = email.subject;
      if (subject.split(' ', 1)[0]  != 'RE:') {
        subject = 'RE: ' + email.subject;
      }

      // Set fields
      document.querySelector('#compose-recipients').value = email.sender;
      document.querySelector('#compose-subject').value = subject;
      document.querySelector('#compose-body').value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
    })
    document.querySelector('#single-email-view').append(reply_button);
  })
}