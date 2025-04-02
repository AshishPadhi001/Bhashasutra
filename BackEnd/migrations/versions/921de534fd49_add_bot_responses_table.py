"""add_bot_responses_table

Revision ID: 921de534fd49
Revises: 3a8b64323890
Create Date: 2025-04-02 10:54:04.318782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '921de534fd49'
down_revision: Union[str, None] = '3a8b64323890'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'bot_responses',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(500), nullable=False),
        sa.Column('response', sa.Text(), nullable=False),
        sa.Column('category', sa.String(100), nullable=False),
        sa.Column('is_faq', sa.Boolean(), default=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_bot_responses_question'), 'bot_responses', ['question'], unique=False)
    op.create_index(op.f('ix_bot_responses_category'), 'bot_responses', ['category'], unique=False)
    
    # Add initial bot FAQs
# Insert predefined FAQ questions
    op.execute("""
    INSERT INTO bot_responses (question, response, category, is_faq) VALUES
    -- General Questions
    ('What is Bhashasutra?', 'Bhashasutra is an NLP-based web application providing text analysis tools such as summarization, sentiment analysis, and text visualization.', 'general', TRUE),
    ('Who made Bhashasutra?', 'Bhashasutra was created by Ashish Padhi and Amit Varma as a project to showcase NLP capabilities in an intuitive web interface.', 'general', TRUE),
    ('What tools does Bhashasutra offer?', 'Bhashasutra has various NLP functionalities categorized into Basic NLP Functions, Advanced NLP Functions, Sentiment Analysis, and Text Visualization.', 'features', TRUE),
    
    -- Basic NLP Functions
    ('What are the basic NLP tools in Bhashasutra?', 'Basic NLP Functions include word counting, punctuation counting, text case conversion, whitespace removal, unique word count, proper noun extraction, and more.', 'basic_nlp', TRUE),
    
    -- Advanced NLP Functions
    ('What are the advanced NLP features in Bhashasutra?', 'Advanced NLP Functions include word/sentence tokenization, stopword removal, stemming, lemmatization, POS tagging, TF-IDF vectorization, text summarization, language detection, and grammar correction.', 'advanced_nlp', TRUE),
    
    -- Sentiment Analysis
    ('Does Bhashasutra support Sentiment Analysis?', 'Yes, Bhashasutra offers sentiment analysis for raw text input, including detailed sentiment reports.', 'sentiment_analysis', TRUE),
    
    -- Text Visualization
    ('What types of text visualizations does Bhashasutra provide?', 'Currently, Bhashasutra provides word clouds, word frequency plots, sentiment distribution graphs, and TF-IDF heatmaps.', 'text_visualization', TRUE),
    
    -- File & Processing Capabilities
    ('Can Bhashasutra process file uploads?', 'Yes, Bhashasutra supports both raw text input and file uploads (PDF, DOC, TXT).', 'file_processing', TRUE),
    ('Does Bhashasutra support real-time NLP processing?', 'It depends on the file size. Small files are processed in real-time, while large files may require batch processing.', 'processing', TRUE),

    -- Future Capabilities
    ('Will Bhashasutra support visualization dashboards?', 'Yes, visualization dashboards are planned for future updates.', 'future_features', TRUE),
    ('Can users customize models or outputs in Bhashasutra?', 'Currently, customization is not available, but it is planned for future updates.', 'future_features', TRUE),

    -- Language & API Usage
    ('Does Bhashasutra support multiple languages?', 'No, Bhashasutra currently supports only English.', 'language_support', TRUE),
    ('Does Bhashasutra use external APIs?', 'Yes, some external APIs are integrated into Bhashasutra.', 'technical', TRUE),

    -- Exit & Other Options
    ('How do I exit Bhashasutra?', 'You can exit Bhashasutra using the "Exit" menu option.', 'usage', TRUE)
    """)


def downgrade() -> None:
    """Downgrade schema."""
    pass
