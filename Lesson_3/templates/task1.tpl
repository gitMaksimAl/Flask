{% extends 'index.html' %}
{% block content %}
<h2><a href="{{ url_for('all_marks') }}">Marks</a></h2>
{% for student in students %}
    <b>{{ student.name }} {{ student.surname }}</b></br>
<pre>    {{ student.id }}
    {{ student.age }}
    {{ student.gender }}
    {{ student.group }}
    {{ student.faculty.name }}
</pre>
{% endfor %}
{% endblock content %}
