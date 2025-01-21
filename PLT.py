import matplotlib.pyplot as plt

# داده‌های نمونه
times = list(range(10))  # زمان‌ها
tasks_completed = [2, 3, 5, 7, 8, 10, 12, 11, 14, 15]  # تعداد کارهای انجام شده

# رسم نمودار
plt.figure(figsize=(10, 5))
plt.plot(times, tasks_completed, marker="o")

# افزودن عنوان و برچسب‌ها
plt.title("Tasks Completed Over Time")
plt.xlabel("Time")
plt.ylabel("Number of Tasks Completed")
plt.xticks(times)  # تعیین مقادیر محور x

# نمایش نمودار
plt.grid()
plt.show()
