document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("login-form");
  const errorMessage = document.getElementById("error-message");

  loginForm.addEventListener("submit", async function (e) {
    e.preventDefault();

    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("/api/token", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({
          username: username,
          password: password,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store token in localStorage
        localStorage.setItem("accessToken", data.access_token);

        // Redirect to dashboard
        window.location.href = "/";
      } else {
        errorMessage.textContent =
          data.detail || "Login failed. Please check your credentials.";
      }
    } catch (error) {
      console.error("Error:", error);
      errorMessage.textContent = "An error occurred. Please try again later.";
    }
  });
});
