import streamlit as st
from quizdata import qz, info_paragraph
from helpersfun import hf_summary, create_Q, openAI_qa


def get_question():
    """ here are the quiz_data defined """
    data = dict()
    data['question'] = qz[st.session_state.form_count][0]
    data['choices'] = qz[st.session_state.form_count][1]
    data['correct_answer'] = qz[st.session_state.form_count][2]
    return data


def initialize_session_state():
    session_state = st.session_state
    session_state.form_count = 0
    session_state.quiz_data = get_question()


def main():
    tab1, tab2 = st.tabs(["Quiz App", "Create questions"])
    with tab1:

        st.title('Choose your answer :monkey:')
        st.divider()

        st.markdown("""
        <style>
            [data-testid=stSidebar] {
                background-color: #ff000050;
            }
        </style>
        """, unsafe_allow_html=True)

        with st.sidebar:
                st.write(":ladybug: Welcome to the quiz that tests :llama: your knowledge about animals. :monkey: \n\n"
                         "There are various types of questions like multiple choice,"
                         " questions involving pictures :frame_with_picture: or maps. Sometimes there is an explanation displayed at the end containing information on the topic of the question."
                         " Have fun guessing when you don't know the answer :sparkles:")
                # st.markdown()

        if 'form_count' not in st.session_state:
            initialize_session_state()
        if not st.session_state.quiz_data:
            st.session_state.quiz_data = get_question()

        quiz_data = st.session_state.quiz_data      # looks like quiz_data['question']['choices']['correct_answer']

        st.markdown(f"Question: {quiz_data['question']}")


        # display images
        if st.session_state.form_count == 3:
            images = ["/home/aliki/PycharmProjects/animals/images/pileatedwoodpecker_female.png", "/home/aliki/PycharmProjects/animals/images/pileatedwoodpecker_male.png"]
            st.image(images, width=400)


        form = st.form(key=f"quiz_form_{st.session_state.form_count}")
        user_choice = form.radio("_Click the correct answer:_", quiz_data['choices'], help="There is only one correct choice")
        submitted = form.form_submit_button("Submit your answer")

        if submitted:
            if user_choice == quiz_data['correct_answer']:
                st.success("Correct")
            else:
                st.error("Incorrect")

            another_question = st.button("Another question")
            if not another_question:    # even though counterintuitive works correctly with if not
                st.session_state.form_count = st.session_state.form_count + 1
                #st.write("inside if", st.session_state.form_count)
                if st.session_state.form_count >= len(qz):
                    st.warning("The questions end here. Time for a coffee, enough knowledge :)")
                    st.stop()
            with st.spinner("Calling the model fo the next question"):
                session_state = st.session_state
                session_state.quiz_data = get_question()

        with tab2:

            st.title('Create your quiz data :monkey:')
            st.divider()

            # A selectboox for choosing OpenAI or another free model from hf
            option = st.selectbox(
                "Which framework would you like to use to create questions? Note: Huggingface is for free and requires some extra writing, OpenAI induces costs as it needs an OpenAI key and delivers directly result",
                ("Huggingface", "OpenAI"),
            )

            st.write("You selected:", option)

            text = st.text_area(
                'You will create a question based on a piece of information. Let AI select the content which is worth creating a question for and then type the question'
                ' and the 4 possible answers yourself. Now dump a paragraph of information about animals',
                placeholder=info_paragraph, max_chars=1050, height=300)

            summarized = None

            if option == "Huggingface":
                summarized = hf_summary(text)
                # maybe it needs a button to show only after the input text
                st.write(summarized)
                question_llm = ""
                if st.button("Create Q"):
                    question_llm = create_Q(summarized)
                    st.write("Q: " + question_llm[0]["generated_text"])
                question = st.text_area("Type a question for the quiz", placeholder=question_llm, max_chars=150, height=50)
                question = st.text_input("Type a question for the quiz", "Where do kangaroos live?")
                answers = st.text_input("Type four possible answers where 1 is true and 3 false", "Germany, Brazil, Australia, Austria")
                correct_answer = st.text_input("The true answer is", "Australia")
                # asnwers, and correct answer in pandas
            else:
                openai_key = st.text_input("Insert your OpenAI key", "007")
                qa = openAI_qa(text, openai_key)
                st.write("Interesting QA for the quiz, right?", qa)
                question = st.text_input("Type a question for the quiz", "Where do kangaroos live?")
                answers = st.text_input("Type four possible answers where 1 is true and 3 false",
                                        "Germany, Brazil, Australia, Austria")
                correct_answer = st.text_input("The true answer is", "Australia")


if __name__ == "__main__":
    main()

