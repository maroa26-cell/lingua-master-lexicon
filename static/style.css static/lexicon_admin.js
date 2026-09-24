let currentAction = null;
let currentId = null;
let allEntries = [];
let currentPage = 1;
const pageSize = 10;

// AUTO REFRESH
setInterval(() => fetchEntries(), 10000);

// FETCH ENTRIES
function fetchEntries() {
    fetch("/get_entries")
        .then(res => res.json())
        .then(data => {
            allEntries = data;
            renderTable();
        });
}

// RENDER TABLE
function renderTable() {
    const tbody = document.querySelector("#lexiconTable tbody");
    tbody.innerHTML = "";

    const start = (currentPage - 1) * pageSize;
    const end = start + pageSize;
    const pageItems = allEntries.slice(start, end);

    pageItems.forEach(e => {
        tbody.innerHTML += `
            <tr>
                <td>${e.english}</td>
                <td>${e.swahili}</td>
                <td>${e.category}</td>
                <td>
                    <button class="btn btn-edit" onclick="openEditModal(${e.id})">Edit</button>
                    <button class="btn btn-delete" onclick="openDeleteModal(${e.id})">Delete</button>
                </td>
            </tr>
        `;
    });

    renderPagination();
}

// PAGINATION
function renderPagination() {
    const totalPages = Math.ceil(allEntries.length / pageSize);
    const container = document.getElementById("pagination");

    container.innerHTML = `
        <button onclick="prevPage()" ${currentPage === 1 ? "disabled" : ""}>Previous</button>
        <span>Page ${currentPage} of ${totalPages}</span>
        <button onclick="nextPage()" ${currentPage === totalPages ? "disabled" : ""}>Next</button>
    `;
}

function nextPage() { currentPage++; renderTable(); }
function prevPage() { currentPage--; renderTable(); }

// SEARCH
function filterTable() {
    const input = document.getElementById("searchInput").value.toLowerCase();
    const rows = document.querySelectorAll("#lexiconTable tbody tr");

    rows.forEach(row => {
        row.style.display = row.innerText.toLowerCase().includes(input) ? "" : "none";
    });
}

// TOAST
function showToast(msg) {
    const t = document.createElement("div");
    t.className = "toast";
    t.innerText = msg;
    document.body.appendChild(t);
    setTimeout(() => t.remove(), 3000);
}

// EXPORT CSV
function exportCSV() {
    fetch("/export_csv")
        .then(res => res.json())
        .then(() => showToast("CSV Exported Successfully"));
}

// EXPORT EXCEL
function exportExcel() {
    fetch("/export_excel")
        .then(res => res.json())
        .then(() => showToast("Excel Exported Successfully"));
}

// EXPORT PDF
function exportPDF() {
    fetch("/export_pdf")
        .then(res => res.json())
        .then(() => showToast("PDF Exported Successfully"));
}

// MODAL CONTROL
function openAddModal() {
    currentAction = "add";
    currentId = null;

    document.getElementById("modalTitle").innerText = "Add Entry";
    document.getElementById("modalFields").style.display = "block";
    document.getElementById("deleteConfirm").style.display = "none";

    document.getElementById("modalEnglish").value = "";
    document.getElementById("modalSwahili").value = "";
    document.getElementById("modalCategory").value = "";

    document.getElementById("modalActionBtn").innerText = "Save";
    document.getElementById("mainModal").style.display = "flex";
}

function openEditModal(id) {
    currentAction = "edit";
    currentId = id;

    fetch(`/get_entry/${id}`)
        .then(res => res.json())
        .then(e => {
            document.getElementById("modalTitle").innerText = "Edit Entry";
            document.getElementById("modalFields").style.display = "block";
            document.getElementById("deleteConfirm").style.display = "none";

            document.getElementById("modalEnglish").value = e.english;
            document.getElementById("modalSwahili").value = e.swahili;
            document.getElementById("modalCategory").value = e.category;

            document.getElementById("modalActionBtn").innerText = "Save Changes";
            document.getElementById("mainModal").style.display = "flex";
        });

    showToast("Edit mode activated");
}

function openDeleteModal(id) {
    currentAction = "delete";
    currentId = id;

    document.getElementById("modalTitle").innerText = "Delete Entry";
    document.getElementById("modalFields").style.display = "none";
    document.getElementById("deleteConfirm").style.display = "block";

    document.getElementById("modalActionBtn").innerText = "Delete";
    document.getElementById("mainModal").style.display = "flex";

    showToast("Delete confirmation opened");
}

document.getElementById("modalActionBtn").onclick = function() {
    if (currentAction === "add") saveAdd();
    if (currentAction === "edit") saveEdit();
    if (currentAction === "delete") confirmDelete();
};

function closeModal() {
    document.getElementById("mainModal").style.display = "none";
}

// ADD
function saveAdd() {
    const english = document.getElementById("modalEnglish").value;
    const swahili = document.getElementById("modalSwahili").value;
    const category = document.getElementById("modalCategory").value;

    fetch("/add_entry", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ english, swahili, category })
    })
    .then(() => {
        showToast("Entry Added Successfully");
        closeModal();
        fetchEntries();
    });
}

// EDIT
function saveEdit() {
    const english = document.getElementById("modalEnglish").value;
    const swahili = document.getElementById("modalSwahili").value;
    const category = document.getElementById("modalCategory").value;

    fetch(`/update_entry/${currentId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ english, swahili, category })
    })
    .then(() => {
        showToast("Entry Updated Successfully");
        closeModal();
        fetchEntries();
    });
}

// DELETE
function confirmDelete() {
    fetch(`/delete_entry/${currentId}`, { method: "DELETE" })
        .then(() => {
            showToast("Entry Deleted Successfully");
            closeModal();
            fetchEntries();
        });
}

// INITIAL LOAD
document.addEventListener("DOMContentLoaded", fetchEntries);
