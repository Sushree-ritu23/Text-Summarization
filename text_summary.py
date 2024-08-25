import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

#text = """BTS also known as the Bangtan Boys, is a South Korean boy band formed in 2010. The band consists of Jin, Suga, J-Hope, RM, Jimin, V, and Jungkook, who co-write or co-produce much of their material. Originally a hip hop group, their musical style has evolved to incorporate a wide range of genres, while their lyrics have focused on subjects including mental health, the troubles of school-age youth and coming of age, loss, the journey towards self-love, individualism, and the consequences of fame and recognition. Their discography and adjacent work has also referenced literature, philosophy and psychological concepts, and includes an alternate universe storyline.BTS debuted in 2013 under Big Hit Entertainment with the single album 2 Cool 4 Skool. BTS released their first Korean and Japanese-language studio albums, Dark & Wild and Wake Up respectively, in 2014.BTS released their first Korean and Japanese-language studio albums, Dark & Wild and Wake Up respectively, in 2014. The group's second Korean studio album, Wings (2016), was their first to sell one million copies in South Korea. By 2017, BTS had crossed into the global music market and led the Korean Wave into the United States, becoming the first Korean ensemble to receive a Gold certification from the Recording Industry Association of America (RIAA) for their single "Mic Drop", as well as the first act from South Korea to top the Billboard 200 with their studio album Love Yourself: Tear (2018). In 2020, BTS became one of the few groups since the Beatles (in 1966–1968) to chart four US number-one albums in less than two years, with Love Yourself: Answer (2018) becoming the first Korean album certified Platinum by the RIAA; in the same year, they also became the first all-South Korean act to reach number one on both the Billboard Hot 100 and Billboard Global 200 with their Grammy-nominated single "Dynamite". Follow-up releases "Savage Love", "Life Goes On", "Butter", and "Permission to Dance" made them the fastest act to earn four US number-one singles since Justin Timberlake in 2006."""

def summarizer(rawdocs):
    stopwords=list(STOP_WORDS)
    #print(stopwords)
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(rawdocs)
    #print(doc)
    tokens = [token.text for token in doc]
    # print(tokens)
    word_freq = {}
    for word in doc:
        if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
            if word.text not in word_freq.keys():
                word_freq[word.text] = 1
            else:
                word_freq[word.text] += 1
    # print(word_freq)

    max_freq = max(word_freq.values())
    #print(max_freq)

    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq

    # print(word_freq)

    sent_tokens = [sent for sent in doc.sents]
    # print(sent_tokens)

    sent_scores = {}
    for sent in sent_tokens:
        for word in sent:
            if word.text in word_freq.keys():
                if sent not in sent_scores.keys():
                    sent_scores[sent] = word_freq[word.text]
                else:
                    sent_scores[sent] += word_freq[word.text] 
    #print(sent_scores)

    select_len = int(len(sent_tokens) * 0.3)
    #print(select_len)
    summary = nlargest(select_len, sent_scores, key = sent_scores.get)
    #print(summary)
    final_summary = [word.text for word in summary]
    summary = ' '.join(final_summary)
    #print(text)
    #print(summary)
    #print("Length of original text ",len(text.split(' ')))
    #print("Length of summary text ",len(summary.split(' ')))

    return summary, doc, len(rawdocs.split(' ')), len(summary.split(' '))