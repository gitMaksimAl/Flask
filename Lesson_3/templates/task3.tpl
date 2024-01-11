{% extends 'index.html' %}
{% block content %}
{% for student in student_data %}
<b>{{ student.name }} {{ student.surname }}</b></br>
<pre>    AGE: {{ student.age }}
    EMAIL: {{ student.email }}{% for mark in student.marks %}
    {{ mark.subject_name.upper() }}: {{ mark.mark }}
    {% endfor %}
</pre>
{% endfor %}
{% endblock content %}
