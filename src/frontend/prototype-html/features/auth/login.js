(function () {
  let selectedRole = 'admin';

  document.querySelectorAll('.role-pick').forEach((element) => {
    element.addEventListener('click', () => {
      document.querySelectorAll('.role-pick').forEach((item) => item.classList.remove('active'));
      element.classList.add('active');
      selectedRole = element.dataset.role;
    });
  });

  document.getElementById('loginBtn').addEventListener('click', () => {
    const destination = selectedRole === 'student'
      ? 'src/features/dashboard/student-dashboard.html'
      : 'src/features/dashboard/admin-dashboard.html';

    window.location.href = destination;
  });
})();
