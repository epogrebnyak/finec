"""Use docstring as labels fo Streamlit multipage app.

Would not work until June - MPA release:

https://github.com/streamlit/streamlit/commit/eca164ae0a0a5316e6da30312638be8ced2c847f
"""
import streamlit as st

def page_1():
    """Page 1"""
    st.markdown("This is Page 1")

def page_2():
    """Page 2""" 
    st.markdown("This is Page 2")

def page_3():
    """Page 3""" 
    st.markdown("This is Page 3")

pages = [(p, p.__doc__) for p in [page_1, page_2, page_3]]
page = st.sidebar.radio(
            'Please choose a page',
            pages,
            format_func=lambda p: p[1])
st.write(page)

"""Exception in thread ScriptRunner.scriptThread:
Traceback (most recent call last):
  File "d:\anaconda3\lib\threading.py", line 932, in _bootstrap_inner
    self.run()
  File "d:\anaconda3\lib\threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "d:\finec\.venv\lib\site-packages\streamlit\scriptrunner\script_runner.py", line 253, in _run_script_thread
    widget_states = self._session_state.as_widget_states()
  File "d:\finec\.venv\lib\site-packages\streamlit\state\session_state.py", line 584, in as_widget_states
    return self._new_widget_state.as_widget_states()
  File "d:\finec\.venv\lib\site-packages\streamlit\state\session_state.py", line 249, in as_widget_states
    states = [
  File "d:\finec\.venv\lib\site-packages\streamlit\state\session_state.py", line 252, in <listcomp>
    if self.get_serialized(widget_id)
  File "d:\finec\.venv\lib\site-packages\streamlit\state\session_state.py", line 230, in get_serialized
    serialized = metadata.serializer(item.value)
  File "d:\finec\.venv\lib\site-packages\streamlit\elements\radio.py", line 167, in serialize_radio
    return index_(options, v)
  File "d:\finec\.venv\lib\site-packages\streamlit\util.py", line 129, in index_
    raise ValueError("{} is not in iterable".format(str(x)))
ValueError: (<function page_3 at 0x000002968E7CB8B0>, 'Page 3') is not in iterable
"""

