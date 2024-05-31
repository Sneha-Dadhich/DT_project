from flask import render_template, request
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
import wikipedia
import random
import requests
from flask import Flask, render_template, request, jsonify, send_file
from apps.chat_history.chat_history_DBadder import add_search_to_database, find_user_id_by_username
from apps.home import blueprint
from apps.chat_history.chat_history_DBadder import dropdown_data, search_data

responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you?": ["I'm good, thank you!", "I'm doing well, thanks for asking.", "All good!"],
    "what is your name?": ["I'm just a humble chatbot.", "I'm your friendly neighborhood bot!", "You can call me ChatBot."],
    "bye": ["Goodbye!", "See you later!", "Bye! Take care!"]
}

def fetch_wiki_results(user_input):
    try:
        result = wikipedia.summary(user_input, sentences=5)
        return result
    except (wikipedia.exceptions.PageError, wikipedia.exceptions.DisambiguationError):
        return "Sorry, result not found"
    except requests.exceptions.ConnectionError:
        return "Sorry, there is no internet connection"
    except wikipedia.exceptions.WikipediaException:
        pass

@blueprint.route('/index')
@login_required
def index():

    return render_template('home/index.html', 
                           segment='index', 
                           user_id=current_user.id)


@blueprint.route('/<template>')
@login_required
def route_template(template):

    try:
        if template=="dashboard":
            pass
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500

@blueprint.route('/dashboard.html',methods=["POST"])
@login_required
def chatbot():
    if request.method == "POST":
        input_text = request.form.get("chat_input")
        if not input_text:
            return jsonify({"error": "No input provided"}), 400

        input_text = input_text.lower()
        #file_url = f"C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\chatBot_for_sir_code\\{username}.csv"
        try:
            if input_text in responses.keys():
                chatBot_answer = random.choice(responses[input_text])
                add_search_to_database(input_text,chatBot_answer,None)
                return jsonify({"response": chatBot_answer})
            else:
                results = fetch_wiki_results(input_text)
                add_search_to_database(input_text,results,None)
                return jsonify({"response": results})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return render_template("home/dashboard.html")



@blueprint.route("/get_years")
def get_years():
    try:
        year = dropdown_data("year")
        return jsonify(year)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint.route("/get_months", methods=["GET"])
def get_months():
    try:
        if request.method=="GET":
            year = request.args.get('yearDropdown', type=int)
            if year!=None:
                month = dropdown_data("month", selected_year=year)
                return jsonify(month)
            if year is None:
                return jsonify({"error": "Year parameter is required"}), 400
            
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint.route("/get_days", methods=["GET"])
def get_days():
    try:
        if request.method=="GET":
            year = request.args.get('yearDropdown', type=int)
            month = request.args.get('monthDropdown', type=int)
        
            if year!=None and month!=None:
                day = dropdown_data("day", selected_year=year, selected_month=month)
                return jsonify(day)
        
        if year is None or month is None:
            return jsonify({"error": "Year and Month parameters are required"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@blueprint.route('/searched_data',methods=['GET'])    
def chat_data():
    if request.method=="GET":
        year = request.form.get("yearDropdown", type=int)
        month = request.form.get("monthDropdown", type=int)
        day = request.form.get("dayDropdown", type=int)
            
        print(f"year: {year} \nmonth: {month} \nday: {day}")
        print("test 1 : passed")
        
        search_data('question',year,month,day)
        return jsonify({"question":search_data})
    
@blueprint.route('/chatBot_history.html')
@login_required
def chat_history():
    render_template("home/chatBot_history.html")

@blueprint.route('/lame.min.js')
def return_lame():
    return send_file('C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\FLASK\\apps\\static\\assets\\js\\lame.min.js')

@blueprint.route('/recorder.js')
def return_recorder():
    return send_file('C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\FLASK\\apps\\static\\assets\\js\\recorder.js')

@blueprint.route('/script.js')
def return_script():
    return send_file('C:\\Sneha\\Programs1\\Python\\Internship\\DreamTeam\\FLASK\\apps\\static\\assets\\js\\script.js')

@blueprint.route('/transactions.html')
@login_required
def voice_synthesis():
    return render_template("home/transactions.html")
    
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
