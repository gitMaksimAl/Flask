{% extends 'index.html' %}
{% block content %}
{% for book in books %}
<b>{{ book.name }}</b></br>
<pre>    {{ book.id }}
    {{ book.year }}
    {{ book.author }}
    {{ book.copies }}
</pre>
{% endfor %}
{% endblock content %}
