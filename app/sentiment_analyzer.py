import praw
import re
import csv
import os
from textblob import TextBlob
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for Matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter


class RedditSentimentAnalysis:

    def __init__(self):
        self.commentText = []

    def clean_comment(self, comment):
        # Remove Links, Special Characters, etc. from the comment
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", comment).split())

    def download_data(self, subreddit_name, num_comments):
        # Authenticating
        client_id = 'client-id'
        client_secret = 'client-secret'
        user_agent = 'user-agent'
        reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

        # Convert num_comments to an integer (with data type check)
        try:
            num_comments = int(num_comments)
        except ValueError:
            print("Invalid input for num_comments. Please enter a valid integer.")
            return None

        # Fetching comments from the specified subreddit
        subreddit = reddit.subreddit(subreddit_name)
        comment_data = subreddit.comments(limit=num_comments)

        # Open/create a file to append data to
        csv_file = open('reddit_result.csv', 'a', newline='', encoding='utf-8')
        csv_writer = csv.writer(csv_file)

        # Create variables to store sentiment counts
        sentiment_ranges = [
            ('positive', (0.3, 1.0)),
            ('wpositive', (0.0, 0.3)),
            ('spositive', (0.6, 1.0)),
            ('neutral', (-0.3, 0.3)),
            ('negative', (-1.0, -0.3)),
            ('wnegative', (-0.3, 0.0)),
            ('snegative', (-1.0, -0.6))
        ]

        sentiment_counts = {sentiment: 0 for sentiment, _ in sentiment_ranges}

        total_polarity = 0.0

        # Iterating through comments fetched
        for comment in comment_data:
            cleaned_comment = self.clean_comment(comment.body)
            self.commentText.append(cleaned_comment)
            analysis = TextBlob(cleaned_comment)

            # Calculate polarity and update sentiment counts
            polarity = analysis.sentiment.polarity
            total_polarity += polarity

            for sentiment, (start_range, end_range) in sentiment_ranges:
                if start_range < polarity <= end_range:
                    sentiment_counts[sentiment] += 1

        # Write cleaned comment data to CSV
        csv_writer.writerow(self.commentText)
        csv_file.close()

        # Calculate percentages
        total_comments = len(self.commentText)
        sentiment_percentages = {sentiment: count / total_comments * 100 for sentiment, count in sentiment_counts.items()}

        # Determine overall sentiment
        overall_sentiment = self.get_overall_sentiment(total_polarity, total_comments)

        # Determine confidence level
        confidence_level = self.calculate_confidence_level(overall_sentiment, total_polarity)

        # Keyword frequency
        keyword_freq = self.calculate_keyword_frequency(3)

        # Generate and save pie chart
        pie_chart_file_name = self.plot_pie_chart(sentiment_percentages, subreddit_name, num_comments)

        # Generate and save word cloud
        word_cloud_file_name = self.generate_word_cloud(subreddit_name)

        return overall_sentiment, confidence_level, keyword_freq, pie_chart_file_name, word_cloud_file_name

    def get_overall_sentiment(self, total_polarity, total_comments):
        if total_comments == 0:
            return "Neutral"

        average_polarity = total_polarity / total_comments

        if -0.3 <= average_polarity <= 0.3:
            return "Neutral"
        elif 0.3 < average_polarity <= 0.6:
            return "Weakly Positive"
        elif 0.6 < average_polarity <= 1.0:
            return "Strongly Positive"
        elif -0.6 <= average_polarity < -0.3:
            return "Weakly Negative"
        elif -1.0 <= average_polarity < -0.6:
            return "Strongly Negative"
        else:
            return "Neutral"
        
    def calculate_confidence_level(self, overall_sentiment, average_polarity):
        # Define thresholds for confidence level
        positive_threshold = 0.3
        negative_threshold = -0.3

        if overall_sentiment == "Positive" and average_polarity > positive_threshold:
            return "High"
        elif overall_sentiment == "Negative" and average_polarity < negative_threshold:
            return "Low"
        else:
            return "Medium"  # Adjust as needed

    def calculate_keyword_frequency(self, num_top_keywords=5):
        # Calculate keyword frequency from the collected comments
        keyword_frequency = Counter(" ".join(self.commentText).split())

        # Get the top N most frequent keywords
        top_keywords = keyword_frequency.most_common(num_top_keywords)

        return top_keywords

    def plot_pie_chart(self, sentiment_percentages, keyword, tweets):
        labels = [f"{sentiment.capitalize()} [{percentage:.2f}%]" for sentiment, percentage in sentiment_percentages.items()]
        sizes = list(sentiment_percentages.values())
        colors = ['yellowgreen', 'lightgreen', 'darkgreen', 'gold', 'red', 'lightsalmon', 'darkred']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')
        ax.legend(labels, loc="best")
        ax.axis('equal')

        # Save the pie chart image
        image_filename = f"app/static/images/sentiment_pie_chart_{keyword}_{tweets}.png"
        plt.savefig(image_filename, bbox_inches='tight', pad_inches=0)
        plt.close(fig)  # Close the Matplotlib figure to release resources

        return image_filename
    
    def generate_word_cloud(self, subreddit_name):
        # Combine all cleaned comments into a single string
        all_comments_text = " ".join(self.commentText)

        # Generate a word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments_text)

        # Save the word cloud image
        wordcloud_image_filename = f"app/static/images/wordcloud_{subreddit_name}.png"
        wordcloud.to_file(wordcloud_image_filename)

        # Return the word cloud image file path
        return wordcloud_image_filename

