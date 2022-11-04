document.addEventListener('DOMContentLoaded', function() {

    // By default load all posts
    loadFeed('main', 1);

    // Use navbar to toggle between views
    document.querySelector('#all_posts').addEventListener('click', () => loadFeed('main', 1));
    if (document.querySelector('#following')) {
        document.querySelector('#following').addEventListener('click', () => loadFeed('following', 1));
    }
    if (document.querySelector('#current_user').innerHTML != 'Not signed in') {
        document.querySelector('#current_user').addEventListener('click', () => showProfile(document.querySelector('#current_user').innerHTML));
    }

    document.querySelector('#add_post_form').addEventListener('submit', addPost);
});

function addPost(event) {

    // Get user input
    const content = document.querySelector('#new_post_textarea').value;

    // Send email to backend
    fetch('/add', {
        method: 'POST',
        body: JSON.stringify({
            content: content
        })
    })
    .then(() => {document.querySelector('#new_post_textarea').value = ''})
    .then(() => {loadFeed('main', 1)});
}

function loadFeed(feed, page) {

    // Clear the current feed
    document.querySelector('#posts').innerHTML = `
    <h2 id="feed_name">&nbsp&nbsp&nbspFeed: ${feed.charAt(0).toUpperCase() + feed.slice(1)}</h2>
    <h2 id="paging_header">&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbspPages:</h3>
    `;

    // Show the feed and hide other views
    document.querySelector('#posts').style.display = 'block';
    document.querySelector('#add').style.display = 'block';
    document.querySelector('#profile').style.display = 'none';

    // Get the appropriate posts
    fetch(`/posts/${feed}/${page}`)
    .then(response => response.json())
    .then(response => {
        console.log(response);

        // Build page navigator 
        num_pages = response.num_pages;

        post_container = document.querySelector('#posts');
        page_nav = document.createElement('nav');
        page_nav.id = "page_nav";
        page_ul = document.createElement('ul');
        page_ul.id = "page_ul";
    
        for (let i = 1; i <= num_pages; i++) {
            let page_li = document.createElement('li');
            page_li.innerHTML = i;
            page_li.className = 'page_li';
            page_li.addEventListener('click', () => {
                loadFeed(feed, i);
            })
            page_ul.append(page_li);
        }
        page_nav.append(page_ul);
        post_container.append(page_nav)


        // Loop over all of the posts
        response.posts.forEach(post => {

            // Create the HTML for each post
            const post_div = document.createElement('div');
            post_div.className = 'post_div';
            post_div.id = post.id;
            post_div.innerHTML = `
                <h3 id="post_content">${post.content}</h3>
                <h1 id= "post_creator">${post.creator}</h1>
                <h2 id="post_time">${post.time}</h2>
                <h4 id="post_likes">${post.likes_count}</h4>
            `;

            // Click on name renders profile functionality
            if (document.querySelector('#current_user').innerHTML !== 'Anonymous') {
                post_div.querySelector('#post_creator').addEventListener('click', () => {
                    showProfile(post.creator);
                })
            } else {
                post_div.querySelector('#post_creator').addEventListener('click', () => {
                    alert("You must be signed in to view profiles.");
                })
            }

            // Add edit functionality
            if (document.querySelector('#current_user').innerHTML === post.creator) {
                const edit_div = document.createElement('div');
                edit_div.className = 'edit_div';
                edit_div.innerHTML = `<p id="edit" style="color: blue;">Edit</p>`;
                edit_div.querySelector('#edit').addEventListener('click', () => {
                    post_div.querySelector('#post_content').innerHTML = `
                        <textarea id="edited">${post.content}</textarea>
                    `;
                    edit_div.innerHTML = `<button id="change_post">Create change</button>`;
                    edit_div.querySelector('#change_post').addEventListener('click', () => {
                        const new_content = post_div.querySelector('#edited').value;
                        fetch(`/post/${post.id}`, {
                            method: 'PUT',
                            body: JSON.stringify({
                              content: new_content
                            })
                          })
                        .then(() => {
                            post_div.querySelector('#post_content').innerHTML = new_content;
                            edit_div.innerHTML = `<p id="edit" style="color: blue;">Edit</p>`;
                        })
                    })
                })
                post_div.append(edit_div);
            } 
        
            // Add like functionality
            const like_div = document.createElement('div');
            let current_likes = post.likes_count;
            like_div.className = 'like_div';
            like_div.innerHTML = `
                <button id="like_post">Like</button>
            `;
            

            // Check like status
            const current_user = document.querySelector('#current_user').innerHTML;
            post.likes.forEach(liker => {
                if (liker === current_user) {
                    like_div.querySelector('#like_post').innerHTML = 'Unlike'
                }
            })

            // Add click event
            like_div.querySelector('#like_post').addEventListener('click', () => {
                fetch(`/like/${post.id}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                        like: post.id
                    })
                })
                .then(() => {
                    state = like_div.querySelector('#like_post').innerHTML;
                    if (state === 'Like') {
                        like_div.querySelector('#like_post').innerHTML = 'Unlike';
                        post_div.querySelector('#post_likes').innerHTML = current_likes + 1;
                        current_likes++;
                    } else {
                        like_div.querySelector('#like_post').innerHTML = 'Like';
                        post_div.querySelector('#post_likes').innerHTML = current_likes - 1;
                        current_likes--;
                    }
                })
            })
            post_div.append(like_div);
            document.querySelector('#posts').append(post_div);
        })
    })
}

function showProfile(username) {

    // Clear past profile
    document.querySelector('#profile').innerHTML = '';

    // Show the feed and hide other views
    document.querySelector('#posts').style.display = 'none';
    document.querySelector('#add').style.display = 'none';
    document.querySelector('#profile').style.display = 'block';

    // Add follow and unfollow functionality
    const current_user = document.querySelector('#current_user').innerHTML;
    
    // Get the profile information from back-end
    fetch(`/profile/${username}`)
    .then(response => response.json())
    .then(profile => {
        console.log(profile)

        // Add followers and following data
        const profile_div = document.createElement('div');
        profile_div.id = 'profile_div';
        profile_div.innerHTML = `
            <h1>${profile.username}</h1>
            <h2>Following: ${profile.following_count}</h2>
            <h2>Followers: ${profile.followers_count}</h2>
        `;

        // Follow functionality
        if (current_user !== username) {

            const button = document.createElement('button');
            button.addEventListener('click', () => {
                fetch(`/profile/${username}`, {
                    method: 'PUT',
                    body: JSON.stringify({
                      follow: username
                    })
                  })
                  .then(() => {showProfile(username)})
            })

            // Check follow status 
            button.innerHTML = 'Follow';
            button.id = 'follow_button';
            button.className = 'btn btn-info';
            profile.followers.forEach(follow => {
            if (current_user === follow) {
                button.innerHTML = 'Unfollow';
            }
        })        
            profile_div.append(button);
        }

        document.querySelector('#profile').append(profile_div);


        // Show message this is your profile
        if (document.querySelector('#follow_button') === null) {
            let message = document.createElement('p');
            message.innerHTML = 'This is your profile';
            message.id = "own_profile_message";
            profile_div.append(message);
        }

        // Add all of the users posts
        profile.posts.forEach(post => {
            const profile_post_div = document.createElement('div');
            profile_post_div.className = 'post_div';
            profile_post_div.innerHTML = `
                <h3 id="post_content">${post.content}</h3>
                <h1 id= "post_creator_profile">~${post.creator}</h1>
                <h2 id="post_time">${post.time}</h2>
                <h4 id="post_likes">${post.likes_count}</h4>
            `;
            document.querySelector('#profile').append(profile_post_div);

        // Add edit functionality
        if (document.querySelector('#current_user').innerHTML === post.creator) {
            const edit_div = document.createElement('div');
            edit_div.className = 'edit_div';
            edit_div.innerHTML = `<p id="edit" style="color: blue;">Edit</p>`;
            edit_div.querySelector('#edit').addEventListener('click', () => {
                profile_post_div.querySelector('#post_content').innerHTML = `
                    <textarea id="edited">${post.content}</textarea>
                `;
                edit_div.innerHTML = `<button id="change_post">Create change</button>`;
                edit_div.querySelector('#change_post').addEventListener('click', () => {
                    const new_content = profile_post_div.querySelector('#edited').value;
                    fetch(`/post/${post.id}`, {
                        method: 'PUT',
                        body: JSON.stringify({
                          content: new_content
                        })
                      })
                    .then(() => {
                        profile_post_div.querySelector('#post_content').innerHTML = new_content;
                        edit_div.innerHTML = `<p id="edit" style="color: blue;">Edit</p>`;
                    })
                })
            })
            profile_post_div.append(edit_div);
        }

        // Add like functionality
        const like_div = document.createElement('div');
        let current_likes = post.likes_count;
        like_div.className = 'like_div';
        like_div.innerHTML = `
            <button id="like_post">Like</button>
        `;
        

        // Check like status
        const current_user = document.querySelector('#current_user').innerHTML;
        post.likes.forEach(liker => {
            if (liker === current_user) {
                like_div.querySelector('#like_post').innerHTML = 'Unlike'
            }
        })

        // Add click event
        like_div.querySelector('#like_post').addEventListener('click', () => {
            fetch(`/like/${post.id}`, {
                method: 'PUT',
                body: JSON.stringify({
                    like: post.id
                })
            })
            .then(() => {
                state = like_div.querySelector('#like_post').innerHTML;
                if (state === 'Like') {
                    like_div.querySelector('#like_post').innerHTML = 'Unlike';
                    profile_post_div.querySelector('#post_likes').innerHTML = current_likes + 1;
                    current_likes++;
                } else {
                    like_div.querySelector('#like_post').innerHTML = 'Like';
                    profile_post_div.querySelector('#post_likes').innerHTML = current_likes - 1;
                    current_likes--;
                }
            })
        })
        profile_post_div.append(like_div);
        document.querySelector('#profile').append(profile_post_div);



        })
    })
}
