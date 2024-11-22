// Biến toàn cục để theo dõi trạng thái "edit" và lưu ID của nhân viên đang chỉnh sửa
let isEditMode = false;
let currentEditId = null;

// Lấy các phần tử HTML
const addEmployeeBtn = document.getElementById("add-employee");
const modal = document.getElementById("addEmployeeModal");
const closeModalBtn = document.querySelector(".close");
const saveEmployeeBtn = document.getElementById("saveEmployee");

// Hiển thị modal khi nhấn nút "Add Employee" và thiết lập chế độ thêm mới
addEmployeeBtn.onclick = function () {
    isEditMode = false; // Chế độ thêm mới
    currentEditId = null; // Không có ID để chỉnh sửa
    document.getElementById("employeeForm").reset(); // Xóa dữ liệu cũ trong form
    modal.style.display = "block";
}

// Ẩn modal khi nhấn nút "Close" (dấu X)
closeModalBtn.onclick = function () {
    modal.style.display = "none";
}

// Ẩn modal khi nhấn ngoài modal
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

// Thêm hành động cho nút "Save" để xử lý cả thêm mới và chỉnh sửa
saveEmployeeBtn.onclick = function () {
    const name = document.getElementById("name").value;
    const position = document.getElementById("position").value;
    const department = document.getElementById("department").value;
    const salary = document.getElementById("salary").value;

    if (name && position && salary) {
        if (isEditMode && currentEditId) {
            // Cập nhật thông tin nhân viên
            fetch('/api/update_employee', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    id: currentEditId,
                    name,
                    position,
                    department,
                    salary
                })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);  // Thông báo thành công
                loadEmployees();      // Cập nhật lại bảng dữ liệu
                document.getElementById("employeeForm").reset();  // Xóa dữ liệu form
                modal.style.display = "none"; // Đóng modal sau khi cập nhật
            })
            .catch(error => console.error('Error:', error));
        } else {
            // Thêm nhân viên mới
            fetch('/api/add_employee', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, position, department, salary })
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);  // Thông báo thành công
                loadEmployees();      // Cập nhật lại bảng dữ liệu
                document.getElementById("employeeForm").reset();  // Xóa dữ liệu form
                modal.style.display = "none"; // Đóng modal sau khi thêm mới
            })
            .catch(error => console.error('Error:', error));
        }
    } else {
        alert("Please fill out all required fields!");
    }
}

// Hàm để tải dữ liệu nhân viên và hiển thị lên bảng
function loadEmployees() {
    fetch('/api/employees')
        .then(response => response.json())
        .then(data => {
            const employeeTable = document.getElementById("employeeTable");
            employeeTable.innerHTML = ""; // Xóa dữ liệu cũ

            data.forEach(employee => {
                const row = document.createElement("tr");

                row.innerHTML = `
                    <td>${employee.id}</td>
                    <td>${employee.name}</td>
                    <td>${employee.position}</td>
                    <td>${employee.department}</td>
                    <td>${employee.salary}</td>
                    <td>
                        <button class="edit-btn" data-id="${employee.id}">Edit</button>
                        <button class="delete-btn" data-id="${employee.id}">Delete</button>
                    </td>
                `;

                employeeTable.appendChild(row);
                
                // Thêm sự kiện cho nút Edit
                row.querySelector(".edit-btn").onclick = function () {
                    isEditMode = true;  // Chế độ chỉnh sửa
                    currentEditId = employee.id; // Lưu ID nhân viên

                    // Điền thông tin vào form
                    document.getElementById("name").value = employee.name;
                    document.getElementById("position").value = employee.position;
                    document.getElementById("department").value = employee.department;
                    document.getElementById("salary").value = employee.salary;

                    // Hiển thị modal
                    modal.style.display = "block";
                };

                // Thêm sự kiện cho nút Delete
                row.querySelector(".delete-btn").onclick = function () {
                    deleteEmployee(employee.id);
                };
            });
        })
        .catch(error => console.error('Error:', error));
}

// Lắng nghe sự kiện nhập vào ô tìm kiếm
document.getElementById("search").addEventListener("input", function() {
    const query = this.value.toLowerCase(); // Lấy giá trị tìm kiếm và chuyển thành chữ thường
    filterEmployees(query); // Gọi hàm filterEmployees để lọc kết quả
});

// Hàm để lọc danh sách nhân viên dựa trên từ khóa
function filterEmployees(query) {
    fetch('/api/employees')
        .then(response => response.json())
        .then(data => {
            const employeeTable = document.getElementById("employeeTable");
            employeeTable.innerHTML = ""; // Xóa dữ liệu cũ

            data
                .filter(employee => 
                    employee.name.toLowerCase().includes(query) || 
                    employee.position.toLowerCase().includes(query)
                )
                .forEach(employee => {
                    const row = document.createElement("tr");

                    row.innerHTML = `
                        <td>${employee.id}</td>
                        <td>${employee.name}</td>
                        <td>${employee.position}</td>
                        <td>${employee.department}</td>
                        <td>${employee.salary}</td>
                        <td>
                            <button class="edit-btn" data-id="${employee.id}">Edit</button>
                            <button class="delete-btn" data-id="${employee.id}">Delete</button>
                        </td>
                    `;

                    employeeTable.appendChild(row);

                    // Sự kiện cho nút Edit
                    row.querySelector(".edit-btn").onclick = function () {
                        isEditMode = true;
                        currentEditId = employee.id;
                        document.getElementById("name").value = employee.name;
                        document.getElementById("position").value = employee.position;
                        document.getElementById("department").value = employee.department;
                        document.getElementById("salary").value = employee.salary;
                        modal.style.display = "block";
                    };

                    // Sự kiện cho nút Delete
                    row.querySelector(".delete-btn").onclick = function () {
                        deleteEmployee(employee.id);
                    };
                });
        })
        .catch(error => console.error('Error:', error));
}


// Hàm để xóa nhân viên
function deleteEmployee(emp_id) {
    fetch(`/api/delete_employee/${emp_id}`, {
        method: 'DELETE'
    })
    .then(response => {
        if (response.ok) {
            loadEmployees(); // Tải lại dữ liệu sau khi xóa thành công
        } else {
            alert("Failed to delete employee.");
        }
    });
}

// Tải dữ liệu nhân viên ngay khi trang được tải
document.addEventListener("DOMContentLoaded", loadEmployees);
