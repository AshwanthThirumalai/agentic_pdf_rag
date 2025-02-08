from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import PDFSearchTool
from pathlib import Path
import PyPDF2
from dotenv import load_dotenv

load_dotenv()

def merge_pdfs(pdf_list, output_filename):
    merger = PyPDF2.PdfMerger()
    
    for pdf in pdf_list:
        merger.append(pdf)
    
    merger.write(output_filename)
    merger.close()
    print(f"Merged PDF saved as {output_filename}")

if __name__ == "__main__":
    output_file = "merged_output.pdf"
    
    # Example list of PDF files
    pdf_files = [
    "VISA_D_Payments.pdf",
    "HDFC_Credit_Cards_B_MITC.pdf",
    "Deloitte_C_Financial_Outlook.pdf",
    "Credit_Cards_A_Sectoral_Analysis.pdf"
	]  # Replace with actual file names
    
    if not pdf_files:
        print("No PDF files provided.")
    else:
        merge_pdfs(pdf_files, output_file)




# Get the directory where the script is located
SCRIPT_DIR = Path(__file__).parent
pdf_path = str(SCRIPT_DIR / "merged_output.pdf")

# Use the resolved path for the PDFSearchTool
pdf_search_tool = PDFSearchTool(pdf=pdf_path)


@CrewBase
class AgenticPdfRag():
	"""AgenticPdfRag crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def pdf_rag_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_rag_agent'],
			tools=[pdf_search_tool],
			verbose=True
		)

	@agent
	def pdf_summary_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['pdf_summary_agent'],
			verbose=True
		)

	@task
	def pdf_rag_task(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_rag_task'],
		)

	@task
	def pdf_summary_task(self) -> Task:
		return Task(
			config=self.tasks_config['pdf_summary_task'],
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the PdfRag crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)