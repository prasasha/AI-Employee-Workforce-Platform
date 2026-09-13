import { useEffect, useState } from "react";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

import "./App.css";

const API_URL = "https://ai-employee-workforce-platform.onrender.com";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const [employees, setEmployees] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [performance, setPerformance] = useState([]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [employeeForm, setEmployeeForm] = useState({
    name: "",
    role: "",
    department: "",
  });

  const [taskForm, setTaskForm] = useState({
    title: "",
    description: "",
    status: "Pending",
    priority: "Medium",
    employee_id: "",
  });

  const [performanceForm, setPerformanceForm] = useState({
    rating: "",
    review: "",
    period: "",
    employee_id: "",
  });

  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [aiLoading, setAiLoading] = useState(false);

  const [insights, setInsights] = useState(null);

  const [risks, setRisks] = useState([]);

  const [smartAssignment, setSmartAssignment] = useState(null);
  const [smartAssignmentLoading, setSmartAssignmentLoading] =
    useState(false);

  // =====================================
  // LOAD ALL DATA
  // =====================================

  useEffect(() => {
    loadAllData();
  }, []);

  const loadAllData = async () => {
    setLoading(true);
    setError("");

    try {
      const [employeesRes, tasksRes, performanceRes] =
        await Promise.all([
          fetch(`${API_URL}/employees/`),
          fetch(`${API_URL}/tasks/`),
          fetch(`${API_URL}/performance/`),
        ]);

      if (!employeesRes.ok) {
        throw new Error("Failed to load employees");
      }

      if (!tasksRes.ok) {
        throw new Error("Failed to load tasks");
      }

      if (!performanceRes.ok) {
        throw new Error("Failed to load performance records");
      }

      const employeesData = await employeesRes.json();
      const tasksData = await tasksRes.json();
      const performanceData = await performanceRes.json();

      setEmployees(employeesData);
      setTasks(tasksData);
      setPerformance(performanceData);
    } catch (err) {
      console.error(err);

      setError(
        "Failed to fetch data. Please check backend server."
      );
    } finally {
      setLoading(false);
    }
  };

  // =====================================
  // EMPLOYEE FUNCTIONS
  // =====================================

  const handleEmployeeChange = (e) => {
    setEmployeeForm({
      ...employeeForm,
      [e.target.name]: e.target.value,
    });
  };

  const addEmployee = async (e) => {
    e.preventDefault();

    try {
      setError("");

      const response = await fetch(`${API_URL}/employees/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(employeeForm),
      });

      if (!response.ok) {
        const data = await response.json();

        throw new Error(
          data.detail || "Failed to add employee"
        );
      }

      setEmployeeForm({
        name: "",
        role: "",
        department: "",
      });

      await loadAllData();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  const deleteEmployee = async (id) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this employee?"
    );

    if (!confirmed) return;

    try {
      setError("");

      const response = await fetch(
        `${API_URL}/employees/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to delete employee");
      }

      await loadAllData();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  // =====================================
  // TASK FUNCTIONS
  // =====================================

  const handleTaskChange = (e) => {
    setTaskForm({
      ...taskForm,
      [e.target.name]: e.target.value,
    });
  };

  const addTask = async (e) => {
    e.preventDefault();

    if (!taskForm.employee_id) {
      setError("Please select an employee.");
      return;
    }

    try {
      setError("");

      const response = await fetch(`${API_URL}/tasks/`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          ...taskForm,
          employee_id: Number(taskForm.employee_id),
        }),
      });

      if (!response.ok) {
        const data = await response.json();

        throw new Error(
          data.detail || "Failed to create task"
        );
      }

      setTaskForm({
        title: "",
        description: "",
        status: "Pending",
        priority: "Medium",
        employee_id: "",
      });

      await loadAllData();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  const deleteTask = async (id) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this task?"
    );

    if (!confirmed) return;

    try {
      setError("");

      const response = await fetch(
        `${API_URL}/tasks/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error("Failed to delete task");
      }

      await loadAllData();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  // =====================================
  // PERFORMANCE FUNCTIONS
  // =====================================

  const handlePerformanceChange = (e) => {
    setPerformanceForm({
      ...performanceForm,
      [e.target.name]: e.target.value,
    });
  };

  const addPerformance = async (e) => {
    e.preventDefault();

    if (!performanceForm.employee_id) {
      setError("Please select an employee.");
      return;
    }

    try {
      setError("");

      const response = await fetch(
        `${API_URL}/performance/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            ...performanceForm,
            rating: Number(performanceForm.rating),
            employee_id: Number(
              performanceForm.employee_id
            ),
          }),
        }
      );

      if (!response.ok) {
        const data = await response.json();

        throw new Error(
          data.detail ||
            "Failed to add performance record"
        );
      }

      setPerformanceForm({
        rating: "",
        review: "",
        period: "",
        employee_id: "",
      });

      await loadAllData();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  const deletePerformance = async (id) => {
    const confirmed = window.confirm(
      "Are you sure you want to delete this performance record?"
    );

    if (!confirmed) return;

    try {
      setError("");

      const response = await fetch(
        `${API_URL}/performance/${id}`,
        {
          method: "DELETE",
        }
      );

      if (!response.ok) {
        throw new Error(
          "Failed to delete performance record"
        );
      }

      await loadAllData();
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  // =====================================
  // AI ASSISTANT
  // =====================================

  const askAI = async () => {
    if (!question.trim()) return;

    setAiLoading(true);
    setError("");

    const currentQuestion = question;

    try {
      const response = await fetch(
        `${API_URL}/ai/assistant?question=${encodeURIComponent(
          currentQuestion
        )}`
      );

      if (!response.ok) {
        throw new Error("AI Assistant failed");
      }

      const data = await response.json();

      const answer = data.answer || {};

      const newEntry = {
        question: data.question || currentQuestion,
        summary: answer.summary || "",
        performance_analysis:
          answer.performance_analysis || "",
        workload_analysis:
          answer.workload_analysis || "",
        risk_level: answer.risk_level || "",
        recommendations:
          answer.recommendations || [],
      };

      setChatHistory((prevHistory) => [
        ...prevHistory,
        newEntry,
      ]);

      setQuestion("");
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setAiLoading(false);
    }
  };

  // =====================================
  // AI INSIGHTS
  // =====================================

  const loadInsights = async () => {
    try {
      setError("");

      const response = await fetch(
        `${API_URL}/ai/workforce-insights`
      );

      if (!response.ok) {
        throw new Error(
          "Failed to load workforce insights"
        );
      }

      const data = await response.json();

      setInsights(data.workforce_insights);
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  // =====================================
  // RISK PREDICTION
  // =====================================

  const loadRisks = async () => {
    try {
      setError("");

      const response = await fetch(
        `${API_URL}/ai/employee-risk-prediction`
      );

      if (!response.ok) {
        throw new Error(
          "Failed to load risk prediction"
        );
      }

      const data = await response.json();

      setRisks(
        data.employee_risk_predictions || []
      );
    } catch (err) {
      console.error(err);
      setError(err.message);
    }
  };

  // =====================================
  // SMART TASK ASSIGNMENT
  // =====================================

  const loadSmartAssignment = async () => {
    setSmartAssignmentLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_URL}/ai/smart-task-assignment`,
        {
          method: "POST",
        }
      );

      if (!response.ok) {
        const data = await response.json();

        throw new Error(
          data.detail ||
            "Failed to generate smart task assignment"
        );
      }

      const data = await response.json();

      setSmartAssignment(data);
    } catch (err) {
      console.error(err);
      setError(err.message);
    } finally {
      setSmartAssignmentLoading(false);
    }
  };

  // =====================================
  // GET EMPLOYEE NAME
  // =====================================

  const getEmployeeName = (id) => {
    const employee = employees.find(
      (emp) => Number(emp.id) === Number(id)
    );

    return employee
      ? employee.name
      : `Employee #${id}`;
  };

  // =====================================
  // PERFORMANCE CHART DATA
  // =====================================

  const performanceChartData = employees.map(
    (employee) => {
      const employeeRecords = performance.filter(
        (item) =>
          Number(item.employee_id) ===
          Number(employee.id)
      );

      const ratings = employeeRecords
        .map((item) => Number(item.rating))
        .filter((rating) => !isNaN(rating));

      const average =
        ratings.length > 0
          ? ratings.reduce(
              (sum, rating) => sum + rating,
              0
            ) / ratings.length
          : 0;

      return {
        name: employee.name,
        performance: Number(
          average.toFixed(2)
        ),
      };
    }
  );

  // =====================================
  // TASK WORKLOAD CHART DATA
  // =====================================

  const taskWorkloadChartData = employees.map(
    (employee) => {
      const employeeTasks = tasks.filter(
        (task) =>
          Number(task.employee_id) ===
          Number(employee.id)
      );

      return {
        name: employee.name,
        tasks: employeeTasks.length,
      };
    }
  );

  // =====================================
  // TASK STATUS CHART DATA
  // =====================================

  const taskStatusChartData = [
    {
      name: "Pending",
      value: tasks.filter(
        (task) =>
          String(task.status).toLowerCase() ===
          "pending"
      ).length,
    },
    {
      name: "In Progress",
      value: tasks.filter(
        (task) =>
          String(task.status).toLowerCase() ===
          "in progress"
      ).length,
    },
    {
      name: "Completed",
      value: tasks.filter(
        (task) =>
          String(task.status).toLowerCase() ===
          "completed"
      ).length,
    },
  ];

  // =====================================
  // DASHBOARD
  // =====================================

  const renderDashboard = () => (
    <>
      <div className="top-header">
        <div>
          <h1>Dashboard 📊</h1>

          <p>
            Manage your workforce with AI-powered
            insights.
          </p>
        </div>

        <div className="profile">
          <div className="profile-icon">M</div>

          <span>Mathiyas</span>
        </div>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Employees</h3>

          <h2>{employees.length}</h2>

          <svg
            width="100%"
            height="24"
            viewBox="0 0 100 24"
            className="sparkline"
          >
            <polyline
              points="0,18 15,16 30,17 45,10 60,12 75,6 100,4"
              fill="none"
              stroke="#e0a458"
              strokeWidth="2"
            />
          </svg>

          <p>Registered employees</p>
        </div>

        <div className="stat-card">
          <h3>Total Tasks</h3>

          <h2>{tasks.length}</h2>

          <svg
            width="100%"
            height="24"
            viewBox="0 0 100 24"
            className="sparkline"
          >
            <polyline
              points="0,10 15,14 30,8 45,15 60,9 75,13 100,7"
              fill="none"
              stroke="#60a5fa"
              strokeWidth="2"
            />
          </svg>

          <p>All assigned tasks</p>
        </div>

        <div className="stat-card">
          <h3>Completed Tasks</h3>

          <h2>
            {
              tasks.filter(
                (task) =>
                  String(task.status).toLowerCase() ===
                  "completed"
              ).length
            }
          </h2>

          <svg
            width="100%"
            height="24"
            viewBox="0 0 100 24"
            className="sparkline"
          >
            <polyline
              points="0,20 15,15 30,16 45,9 60,11 75,5 100,3"
              fill="none"
              stroke="#4ade80"
              strokeWidth="2"
            />
          </svg>

          <p>Successfully completed</p>
        </div>

        <div className="stat-card">
          <h3>Performance Records</h3>

          <h2>{performance.length}</h2>

          <svg
            width="100%"
            height="24"
            viewBox="0 0 100 24"
            className="sparkline"
          >
            <polyline
              points="0,14 15,12 30,15 45,11 60,13 75,8 100,10"
              fill="none"
              stroke="#e0a458"
              strokeWidth="2"
            />
          </svg>

          <p>Employee reviews</p>
        </div>
      </div>

      <div className="welcome-card">
        <h2>
          Welcome to AI Employee Workforce Platform 🚀
        </h2>

        <p>
          Manage employees, assign tasks, track
          performance and use AI-powered workforce
          intelligence to make better management
          decisions.
        </p>

        <button
          className="primary-btn"
          onClick={() => setActivePage("employees")}
        >
          Manage Employees
        </button>
      </div>

      {/* ===================================== */}
      {/* EMPLOYEE PERFORMANCE CHART */}
      {/* ===================================== */}

      <div
        className="welcome-card"
        style={{ marginTop: "24px" }}
      >
        <h2>
          Employee Performance Analytics 📊
        </h2>

        <p>
          Average performance rating of each employee.
        </p>

        {performanceChartData.length === 0 ? (
          <div className="coming-soon">
            <h3>No employee data available</h3>

            <p>
              Add employees and performance records
              to view the chart.
            </p>
          </div>
        ) : (
          <div
            style={{
              width: "100%",
              height: "350px",
              marginTop: "20px",
            }}
          >
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <BarChart
                data={performanceChartData}
                margin={{
                  top: 20,
                  right: 30,
                  left: 20,
                  bottom: 20,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="name" />

                <YAxis domain={[0, 5]} />

                <Tooltip />

                <Bar
                  dataKey="performance"
                  name="Performance"
                  fill="#e0a458"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* ===================================== */}
      {/* TASK WORKLOAD CHART */}
      {/* ===================================== */}

      <div
        className="welcome-card"
        style={{ marginTop: "24px" }}
      >
        <h2>
          Employee Task Workload Analytics 📋
        </h2>

        <p>
          Number of tasks currently assigned to each
          employee.
        </p>

        {taskWorkloadChartData.length === 0 ? (
          <div className="coming-soon">
            <h3>No employee data available</h3>

            <p>
              Add employees and tasks to view workload
              analytics.
            </p>
          </div>
        ) : (
          <div
            style={{
              width: "100%",
              height: "350px",
              marginTop: "20px",
            }}
          >
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <BarChart
                data={taskWorkloadChartData}
                margin={{
                  top: 20,
                  right: 30,
                  left: 20,
                  bottom: 20,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="name" />

                <YAxis allowDecimals={false} />

                <Tooltip />

                <Bar
                  dataKey="tasks"
                  name="Assigned Tasks"
                  fill="#60a5fa"
                  radius={[6, 6, 0, 0]}
                />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>

      {/* ===================================== */}
      {/* TASK STATUS CHART */}
      {/* ===================================== */}

      <div
        className="welcome-card"
        style={{ marginTop: "24px" }}
      >
        <h2>
          Task Status Analytics 📊
        </h2>

        <p>
          Distribution of tasks based on their current
          status.
        </p>

        {tasks.length === 0 ? (
          <div className="coming-soon">
            <h3>No task data available</h3>

            <p>
              Create tasks to view task status analytics.
            </p>
          </div>
        ) : (
          <div
            style={{
              width: "100%",
              height: "350px",
              marginTop: "20px",
            }}
          >
            <ResponsiveContainer
              width="100%"
              height="100%"
            >
              <PieChart>
                <Pie
                  data={taskStatusChartData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={110}
                  label
                >
                  {taskStatusChartData.map(
                    (entry, index) => (
                      <Cell
                        key={`cell-${index}`}
                      />
                    )
                  )}
                </Pie>

                <Tooltip />

                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        )}
      </div>
    </>
  );

  // =====================================
  // EMPLOYEES PAGE
  // =====================================

  const renderEmployees = () => (
    <>
      <div className="task-top">
        <div>
          <h1>Employee Management 👥</h1>

          <p>Add and manage employees.</p>
        </div>

        <button
          className="refresh-btn"
          onClick={loadAllData}
        >
          Refresh
        </button>
      </div>

      <div className="employee-form">
        <h2>Add New Employee</h2>

        <form onSubmit={addEmployee}>
          <input
            type="text"
            name="name"
            placeholder="Employee Name"
            value={employeeForm.name}
            onChange={handleEmployeeChange}
            required
          />

          <input
            type="text"
            name="role"
            placeholder="Employee Role"
            value={employeeForm.role}
            onChange={handleEmployeeChange}
            required
          />

          <input
            type="text"
            name="department"
            placeholder="Department"
            value={employeeForm.department}
            onChange={handleEmployeeChange}
            required
          />

          <button
            type="submit"
            className="create-btn"
          >
            ➕ Add Employee
          </button>
        </form>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Role</th>
              <th>Department</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {employees.length === 0 ? (
              <tr>
                <td
                  colSpan="5"
                  className="empty-message"
                >
                  No employees found.
                </td>
              </tr>
            ) : (
              employees.map((employee) => (
                <tr key={employee.id}>
                  <td>{employee.id}</td>

                  <td>{employee.name}</td>

                  <td>{employee.role}</td>

                  <td>{employee.department}</td>

                  <td>
                    <button
                      className="delete-btn"
                      onClick={() =>
                        deleteEmployee(employee.id)
                      }
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </>
  );

  // =====================================
  // TASKS PAGE
  // =====================================

  const renderTasks = () => (
    <>
      <div className="task-top">
        <div>
          <h1>Task Management 📋</h1>

          <p>Create and manage employee tasks.</p>
        </div>

        <button
          className="refresh-btn"
          onClick={loadAllData}
        >
          Refresh
        </button>
      </div>

      <div className="task-form-container">
        <h2>Create New Task</h2>

        <form
          className="task-form"
          onSubmit={addTask}
        >
          <input
            type="text"
            name="title"
            placeholder="Task Title"
            value={taskForm.title}
            onChange={handleTaskChange}
            required
          />

          <select
            name="employee_id"
            value={taskForm.employee_id}
            onChange={handleTaskChange}
            required
          >
            <option value="">
              Select Employee
            </option>

            {employees.map((employee) => (
              <option
                key={employee.id}
                value={employee.id}
              >
                {employee.name}
              </option>
            ))}
          </select>

          <select
            name="status"
            value={taskForm.status}
            onChange={handleTaskChange}
          >
            <option>Pending</option>
            <option>In Progress</option>
            <option>Completed</option>
          </select>

          <select
            name="priority"
            value={taskForm.priority}
            onChange={handleTaskChange}
          >
            <option>Low</option>
            <option>Medium</option>
            <option>High</option>
          </select>

          <textarea
            name="description"
            placeholder="Task Description"
            value={taskForm.description}
            onChange={handleTaskChange}
          />

          <button
            type="submit"
            className="create-btn"
          >
            ➕ Create Task
          </button>
        </form>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Status</th>
              <th>Priority</th>
              <th>Employee</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {tasks.length === 0 ? (
              <tr>
                <td
                  colSpan="6"
                  className="empty-message"
                >
                  No tasks found.
                </td>
              </tr>
            ) : (
              tasks.map((task) => (
                <tr key={task.id}>
                  <td>{task.id}</td>

                  <td>{task.title}</td>

                  <td>
                    <span
                      className={`status ${String(
                        task.status
                      )
                        .toLowerCase()
                        .replace(/\s+/g, "-")}`}
                    >
                      {task.status}
                    </span>
                  </td>

                  <td>{task.priority}</td>

                  <td>
                    {getEmployeeName(
                      task.employee_id
                    )}
                  </td>

                  <td>
                    <button
                      className="delete-btn"
                      onClick={() =>
                        deleteTask(task.id)
                      }
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </>
  );

  // =====================================
  // PERFORMANCE PAGE
  // =====================================

  const renderPerformance = () => (
    <>
      <div className="task-top">
        <div>
          <h1>Performance Management 📈</h1>

          <p>
            Track employee performance and reviews.
          </p>
        </div>

        <button
          className="refresh-btn"
          onClick={loadAllData}
        >
          Refresh
        </button>
      </div>

      <div className="employee-form">
        <h2>Add Performance Record</h2>

        <form onSubmit={addPerformance}>
          <select
            name="employee_id"
            value={performanceForm.employee_id}
            onChange={handlePerformanceChange}
            required
          >
            <option value="">
              Select Employee
            </option>

            {employees.map((employee) => (
              <option
                key={employee.id}
                value={employee.id}
              >
                {employee.name}
              </option>
            ))}
          </select>

          <input
            type="number"
            name="rating"
            placeholder="Rating (1-5)"
            min="1"
            max="5"
            step="0.1"
            value={performanceForm.rating}
            onChange={handlePerformanceChange}
            required
          />

          <input
            type="text"
            name="period"
            placeholder="Review Period"
            value={performanceForm.period}
            onChange={handlePerformanceChange}
            required
          />

          <input
            type="text"
            name="review"
            placeholder="Performance Review"
            value={performanceForm.review}
            onChange={handlePerformanceChange}
            required
          />

          <button
            type="submit"
            className="create-btn"
          >
            ➕ Add Performance
          </button>
        </form>
      </div>

      <div className="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Employee</th>
              <th>Rating</th>
              <th>Review</th>
              <th>Period</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            {performance.length === 0 ? (
              <tr>
                <td
                  colSpan="6"
                  className="empty-message"
                >
                  No performance records found.
                </td>
              </tr>
            ) : (
              performance.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>

                  <td>
                    {getEmployeeName(
                      item.employee_id
                    )}
                  </td>

                  <td>{item.rating}</td>

                  <td>{item.review}</td>

                  <td>{item.period}</td>

                  <td>
                    <button
                      className="delete-btn"
                      onClick={() =>
                        deletePerformance(item.id)
                      }
                    >
                      Delete
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </>
  );

  // =====================================
  // AI ASSISTANT PAGE
  // =====================================

  const renderAI = () => (
    <div className="ai-section">
      <div className="ai-header">
        <h2>
          AI Workforce Assistant 🤖
        </h2>

        <p>
          Ask questions about your employees,
          tasks, workload and workforce performance.
        </p>
      </div>

      <div className="chat-container">
        <div className="chat-box">
          {chatHistory.length === 0 ? (
            <div className="placeholder">
              Ask the AI Workforce Assistant a
              question.
            </div>
          ) : (
            chatHistory.map(
              (entry, entryIndex) => (
                <div key={entryIndex}>
                  <div className="chat-message user-message">
                    {entry.question}
                  </div>

                  <div className="chat-message ai-message">
                    <strong>AI Analysis:</strong>

                    <br />
                    <br />

                    {entry.summary}

                    {entry.performance_analysis && (
                      <>
                        <br />
                        <br />

                        <strong>
                          Performance:
                        </strong>

                        <br />

                        {entry.performance_analysis}
                      </>
                    )}

                    {entry.workload_analysis && (
                      <>
                        <br />
                        <br />

                        <strong>
                          Workload:
                        </strong>

                        <br />

                        {entry.workload_analysis}
                      </>
                    )}

                    {entry.risk_level && (
                      <>
                        <br />
                        <br />

                        <strong>
                          Risk Level:
                        </strong>{" "}
                        {entry.risk_level}
                      </>
                    )}

                    {entry.recommendations &&
                      entry.recommendations
                        .length > 0 && (
                        <>
                          <br />
                          <br />

                          <strong>
                            Recommendations:
                          </strong>

                          <ul>
                            {entry.recommendations.map(
                              (
                                recommendation,
                                recIndex
                              ) => (
                                <li
                                  key={recIndex}
                                >
                                  {
                                    recommendation
                                  }
                                </li>
                              )
                            )}
                          </ul>
                        </>
                      )}
                  </div>
                </div>
              )
            )
          )}
        </div>

        <div className="chat-input-container">
          <input
            type="text"
            placeholder="Ask something about your workforce..."
            value={question}
            onChange={(e) =>
              setQuestion(e.target.value)
            }
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                askAI();
              }
            }}
          />

          <button
            onClick={askAI}
            disabled={aiLoading}
          >
            {aiLoading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>
    </div>
  );

  // =====================================
  // AI INSIGHTS PAGE
  // =====================================

  const renderInsights = () => (
    <>
      <div className="task-top">
        <div>
          <h1>
            AI Workforce Insights 🧠
          </h1>

          <p>
            AI-powered analysis of your workforce
            performance, workload and organizational risk.
          </p>
        </div>

        <button
          className="primary-btn"
          onClick={loadInsights}
        >
          Generate Insights
        </button>
      </div>

      {!insights ? (
        <div className="coming-soon">
          <h2>
            Generate Workforce Insights
          </h2>

          <p>
            Click the button above to analyze
            employees, performance and workload.
          </p>

          <div className="coming-soon-icon">
            🧠
          </div>
        </div>
      ) : (
        <>
          <div className="welcome-card">
            <h2>
              Workforce AI Summary 🤖
            </h2>

            <p>
              {insights.summary}
            </p>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <h3>
                📈 Performance Analysis
              </h3>

              <p>
                {insights.performance_analysis}
              </p>
            </div>

            <div className="stat-card">
              <h3>
                📋 Workload Analysis
              </h3>

              <p>
                {insights.workload_analysis}
              </p>
            </div>

            <div className="stat-card">
              <h3>
                ⚠️ Organization Risk
              </h3>

              <h2>
                {insights.risk_level}
              </h2>

              <p>
                Overall workforce risk level
              </p>
            </div>

            <div className="stat-card">
              <h3>
                🤖 AI Status
              </h3>

              <h2>
                Active
              </h2>

              <p>
                Workforce intelligence engine
              </p>
            </div>
          </div>

          <div className="insight-card">
            <h3>
              📈 Performance Analysis
            </h3>

            <p>
              {insights.performance_analysis}
            </p>
          </div>

          <div className="insight-card">
            <h3>
              📋 Workload Analysis
            </h3>

            <p>
              {insights.workload_analysis}
            </p>
          </div>

          <div className="insight-card">
            <h3>
              ⚠️ Organization Risk Level
            </h3>

            <h2>
              {insights.risk_level}
            </h2>

            <p>
              This risk level is calculated using
              workforce workload and performance data.
            </p>
          </div>

          <div className="insight-card">
            <h3>
              💡 AI Recommendations
            </h3>

            <ul>
              {(insights.recommendations || []).map(
                (item, index) => (
                  <li key={index}>
                    {item}
                  </li>
                )
              )}
            </ul>
          </div>
        </>
      )}
    </>
  );

  // =====================================
  // RISK PREDICTION PAGE
  // =====================================

  const renderRiskPrediction = () => (
    <>
      <div className="task-top">
        <div>
          <h1>
            Employee Risk Prediction ⚠️
          </h1>

          <p>
            Analyze workload and performance risks.
          </p>
        </div>

        <button
          className="primary-btn"
          onClick={loadRisks}
        >
          Analyze Risks
        </button>
      </div>

      {risks.length === 0 ? (
        <div className="coming-soon">
          <h2>
            Employee Risk Analysis
          </h2>

          <p>
            Click Analyze Risks to generate
            workforce risk predictions.
          </p>

          <div className="coming-soon-icon">
            ⚠️
          </div>
        </div>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>Employee</th>
                <th>Department</th>
                <th>Performance</th>
                <th>Tasks</th>
                <th>Completed</th>
                <th>Risk</th>
              </tr>
            </thead>

            <tbody>
              {risks.map((risk) => (
                <tr key={risk.employee_id}>
                  <td>
                    {risk.employee_name}
                  </td>

                  <td>
                    {risk.department}
                  </td>

                  <td>
                    {risk.performance_score}
                  </td>

                  <td>
                    {risk.assigned_tasks}
                  </td>

                  <td>
                    {risk.completed_tasks}
                  </td>

                  <td>
                    <span
                      className={`risk-badge ${String(
                        risk.risk_level
                      ).toLowerCase()}`}
                    >
                      {risk.risk_level}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </>
  );

  // =====================================
  // SMART TASK ASSIGNMENT PAGE
  // =====================================

  const renderSmartAssignment = () => (
    <>
      <div className="task-top">
        <div>
          <h1>
            Smart Task Assignment 🎯
          </h1>

          <p>
            AI-powered task assignment based on
            workload, performance and completed tasks.
          </p>
        </div>

        <button
          className="primary-btn"
          onClick={loadSmartAssignment}
          disabled={smartAssignmentLoading}
        >
          {smartAssignmentLoading
            ? "Analyzing..."
            : "Find Best Employee"}
        </button>
      </div>

      {!smartAssignment ? (
        <div className="coming-soon">
          <h2>
            Find the Best Employee
          </h2>

          <p>
            The AI engine will analyze employee
            workload, performance and completed tasks.
          </p>

          <div className="coming-soon-icon">
            🎯
          </div>
        </div>
      ) : (
        <>
          <div className="welcome-card">
            <h2>
              Recommended Employee 👤
            </h2>

            <h1>
              {
                smartAssignment
                  .recommended_employee
                  ?.name
              }
            </h1>

            <p>
              Role:{" "}
              {
                smartAssignment
                  .recommended_employee
                  ?.role
              }
            </p>

            <p>
              Department:{" "}
              {
                smartAssignment
                  .recommended_employee
                  ?.department
              }
            </p>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <h3>
                Current Workload
              </h3>

              <h2>
                {smartAssignment.current_workload}
              </h2>

              <p>
                Assigned active tasks
              </p>
            </div>

            <div className="stat-card">
              <h3>
                Performance Score
              </h3>

              <h2>
                {smartAssignment.performance_score}
              </h2>

              <p>
                Average performance rating
              </p>
            </div>

            <div className="stat-card">
              <h3>
                Completed Tasks
              </h3>

              <h2>
                {smartAssignment.completed_tasks}
              </h2>

              <p>
                Successfully completed
              </p>
            </div>

            <div className="stat-card">
              <h3>
                Smart Score
              </h3>

              <h2>
                {smartAssignment.smart_score}
              </h2>

              <p>
                AI assignment score
              </p>
            </div>
          </div>

          <div className="table-container">
            <h2
              style={{
                padding: "20px 20px 10px",
                margin: 0,
              }}
            >
              Employee Assignment Analysis 👥
            </h2>

            <table>
              <thead>
                <tr>
                  <th>Rank</th>
                  <th>Employee</th>
                  <th>Role</th>
                  <th>Department</th>
                  <th>Workload</th>
                  <th>Performance</th>
                  <th>Completed</th>
                  <th>Smart Score</th>
                </tr>
              </thead>

              <tbody>
                {(
                  smartAssignment.all_employees || []
                ).map((employee, index) => (
                  <tr key={employee.id}>
                    <td>
                      {index === 0
                        ? "🥇"
                        : index === 1
                        ? "🥈"
                        : index === 2
                        ? "🥉"
                        : index + 1}
                    </td>

                    <td>
                      <strong>
                        {employee.name}
                      </strong>

                      {employee.id ===
                        smartAssignment
                          .recommended_employee
                          ?.id && (
                        <span
                          style={{
                            marginLeft: "8px",
                          }}
                        >
                          ⭐ Recommended
                        </span>
                      )}
                    </td>

                    <td>
                      {employee.role}
                    </td>

                    <td>
                      {employee.department}
                    </td>

                    <td>
                      {employee.current_workload}
                    </td>

                    <td>
                      {employee.performance_score}
                    </td>

                    <td>
                      {employee.completed_tasks}
                    </td>

                    <td>
                      <strong>
                        {employee.smart_score}
                      </strong>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="insight-card">
            <h3>
              AI Recommendation
            </h3>

            <p>
              {smartAssignment.reason}
            </p>
          </div>
        </>
      )}
    </>
  );

  // =====================================
  // PAGE RENDERER
  // =====================================

  const renderPage = () => {
    switch (activePage) {
      case "dashboard":
        return renderDashboard();

      case "employees":
        return renderEmployees();

      case "tasks":
        return renderTasks();

      case "performance":
        return renderPerformance();

      case "ai":
        return renderAI();

      case "insights":
        return renderInsights();

      case "risk":
        return renderRiskPrediction();

      case "smart-assignment":
        return renderSmartAssignment();

      default:
        return renderDashboard();
    }
  };

  // =====================================
  // MAIN APP
  // =====================================

  return (
    <div className="app-container">
      <aside className="sidebar">
        <div className="logo">
          <h2>
            AI Workforce
          </h2>

          <span>
            Management Platform
          </span>
        </div>

        <nav>
          <button
            className={`nav-item ${
              activePage === "dashboard"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("dashboard")
            }
          >
            📊 Dashboard
          </button>

          <button
            className={`nav-item ${
              activePage === "employees"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("employees")
            }
          >
            👥 Employees
          </button>

          <button
            className={`nav-item ${
              activePage === "tasks"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("tasks")
            }
          >
            📋 Tasks
          </button>

          <button
            className={`nav-item ${
              activePage === "performance"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("performance")
            }
          >
            📈 Performance
          </button>

          <button
            className={`nav-item ${
              activePage === "ai"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("ai")
            }
          >
            🤖 AI Assistant
          </button>

          <button
            className={`nav-item ${
              activePage === "insights"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("insights")
            }
          >
            🧠 AI Insights
          </button>

          <button
            className={`nav-item ${
              activePage === "risk"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage("risk")
            }
          >
            ⚠️ Risk Prediction
          </button>

          <button
            className={`nav-item ${
              activePage === "smart-assignment"
                ? "active"
                : ""
            }`}
            onClick={() =>
              setActivePage(
                "smart-assignment"
              )
            }
          >
            🎯 Smart Assignment
          </button>
        </nav>

        <div className="sidebar-bottom">
          AI Employee Workforce Platform
        </div>
      </aside>

      <main className="main-content">
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading && (
          <div className="loading-message">
            Loading data...
          </div>
        )}

        {renderPage()}
      </main>
    </div>
  );
}

export default App;