
# import os
# from src.retrieval_model import MedicalQARetrievalModel
#
# def run_chatbot():
#     print("chatbot in initalizingg..")
#     data_path = "data/processed_medquad_qa.csv"
#
#     try:
#         model = MedicalQARetrievalModel(data_path=data_path)
#         print("\nChatbot intiliaze exit to quit")
#         print("asme me anything related to medical")
#
#         while True:
#             user_query = input("\nYou: ")
#             if user_query.lower() == 'exit':
#                 print("see you soon")
#                 break
#             answers = model.get_answer(user_query, top_k=3)
#
#             if answers:
#                 top_ans = answers[0]
#                 print(f"\nChatbot (Best Match - Similarity: {top_ans['similarity_score']:.4f}):")
#                 print(f"  Question Found: {top_ans['question']}")
#                 print(f"  Answer: {top_ans['answer']}")
#
#                 if len(answers) > 1:
#                     print("\nother relavent answer you might be loooking for")
#                     for i, ans in enumerate(answers[1:]):
#                          print(f"  Match {i + 2} (Similarity: {ans['similarity_score']:.4f}):")
#                          print(f"    Question Found: {ans['question']}")
#                          print(f"    Answer: {ans['answer'][:150]}...")
#                          print("-" * 20)
#                 else:
#                     print("Chatbot: I couldn't find a relevant answer to your question. Please try rephrasing or asking something else.")
#
#     except FileNotFoundError as e:
#         print(f"Error: {e}")
#         print("Please ensure you have run 'data_loaders.py'.")
#     except ValueError as e:
#         print(f"Error: {e}")
#         print("The processed data file might be empty or corrupted.")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#         print("Please check the console for details or restart the chatbot.")
#
#
# if __name__ == "__main__":
#     run_chatbot()
