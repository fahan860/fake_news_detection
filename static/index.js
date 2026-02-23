
   const signUpBtn = document.getElementById('signUp');
   const signInBtn = document.getElementById('LogIn');
   const container = document.getElementById('container');

   signUpBtn.addEventListener('click', () => {
       container.classList.add('right-panel-active');
   });

   signInBtn.addEventListener('click', () => {
       container.classList.remove('right-panel-active');
   });

   function togglePassword() {
       const passwordInputs = document.querySelectorAll(".passwordInput");
       const eyeIcons = document.querySelectorAll(".toggle-eye");

       passwordInputs.forEach((passwordInput, index) => {
           const eyeIcon = eyeIcons[index];
           if (passwordInput.type === "password") {
               passwordInput.type = "text";
               eyeIcon.textContent = "👁️";
           } else {
               passwordInput.type = "password";
               eyeIcon.textContent = "🙈";
           }
       });
   }

   async function signup() {
       console.log("Signup function called");
       const form = document.getElementById('signup-form');
       const formData = new FormData(form);
       const data = {
           username: formData.get('username'),
           email: formData.get('email'),
           password: formData.get('password')
       };
       console.log("Signup data:", data);

       try {
           console.log("Making signup request...");
           const response = await fetch('/api/signup', {
               method: 'POST',
               headers: { 'Content-Type': 'application/json' },
               body: JSON.stringify(data)
           });
           console.log("Signup response status:", response.status);
           const result = await response.json();
           console.log("Signup response data:", result);
           if (response.ok) {
               alert('Account created! Please log in.');
               container.classList.remove('right-panel-active');
           } else {
               alert(result.message);
           }
       } catch (error) {
           console.error("Signup error:", error);
           alert('Error: ' + error.message);
       }
   }

   async function signin() {
       console.log("Signin function called");
       const form = document.getElementById('signin-form');
       const formData = new FormData(form);
       const data = {
           email: formData.get('email'),
           password: formData.get('password')
       };
       console.log("Signin data:", data);

       try {
           console.log("Making signin request...");
           const response = await fetch('/api/login', {
               method: 'POST',
               headers: { 'Content-Type': 'application/json' },
               body: JSON.stringify(data)
           });
           console.log("Signin response status:", response.status);
           const result = await response.json();
           console.log("Signin response data:", result);
           if (response.ok) {
            window.location.href = '/fake_news_interface.html';
           } else {
               alert(result.message);
           }
       } catch (error) {
           console.error("Signin error:", error);
           alert('Error: ' + error.message);
       }
   }
   