from discord.ext import tasks, commands
import http3
import random

class RandomCommands(commands.Cog, name='Random Commands'):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):  
        return (ctx.author.guild_permissions.administrator or ctx.channel.name=='reap-discussion') and not ctx.author.bot

    @commands.command(name='kanye',help='Authentic Kanye West quote')
    async def kanye(self,ctx):
        cli = http3.AsyncClient()
        r = await cli.get("https://api.kanye.rest")
        await ctx.send(f"\"{r.json()['quote']}\"")

    @commands.command(name='chuck',help='Get a Chuck Norris related joke')
    async def chuck(self,ctx):
        cli = http3.AsyncClient()
        r = await cli.get("https://geek-jokes.sameerkumar.website/api?format=json")
        await ctx.send(f"\"{r.json()['joke']}\"")

    @commands.command(name='trump',help='Authentic Donald Trump quotes')
    async def trump(self,ctx):
        cli = http3.AsyncClient()
        r = await cli.get("https://www.tronalddump.io/random/quote")
        json = r.json()
        text = f"\"{json['value']}\" *({json['appeared_at'][:4]})*"
        await ctx.send(text)

    @commands.command(name='elon',help='Authentic Elon Musk quotes')
    async def elon(self,ctx):
        ELON = [
            "Physics is a good framework for thinking. Boil things down to their fundamental truths and reason up from there.",
            "As a child I would just question things...",
            "Any product that needs a manual to work is broken.",
            "America is the spirit of human exploration distilled.",
            "As much as possible, avoid hiring MBAs. MBA programs don’t teach people how to create companies.",
            "Brand is just a perception, and perception will match reality over time.",
            "Being an entrepreneur is like eating glass and staring into the abyss of death.",
            "Brand is just a perception, and perception will match reality over time. Sometimes it will be ahead, other times it will be behind. But brand is simply a collective impression some have about a product.",
            "Being an Entrepreneur is like eating glass and staring into the abyss of death",
            "Constantly seek criticism. A well thought out critique of whatever you’re doing is as valuable as gold.",
            "Constantly think about how you could be doing things better.",
            "Don’t delude yourself into thinking something’s working when it’s not, or you’re gonna get fixated on a bad solution.",
            "Don’t be afraid of new arenas.",
            "Every person in your company is a vector. Your progress is determined by the sum of all vectors.  ",
            "Failure is an option here. If things are not failing, you are not innovating enough.",
            "Great companies are built on great products.",
            "Going from PayPal, I thought: ‘Well, what are some of the other problems that are likely to most affect the future of humanity?’ Not from the perspective, ‘What’s the best way to make money?",
            "It is important to view knowledge as sort of a semantic tree -- make sure you understand the fundamental principles, ie the trunk and big branches, before you get into the leaves/details or there is nothing for them to hang on to.",
            "I think it would be great to be born on Earth and die on Mars. Just hopefully not at the point of impact.",
            "I think it's very important to have a feedback loop, where you're constantly thinking about what you've done and how you could be doing it better.",
            "I think it’s important to reason from first principles rather than by analogy. The normal way we conduct our lives is we reason by analogy. [With analogy] we are doing this because it’s like something else that was done, or it is like what other people are doing. [With first principles] you boil things down to the most fundamental truths...and then reason up from there.",
            "I'm not trying to be anyone's savior. I'm just trying to think about the future and not be sad.",
            "It is possible for ordinary people to choose to be extraordinary.",
            "If you need inspiration, don't do it.",
            "I came to the conclusion that we should aspire to increase the scope and scale of human consciousness in order to better understand what questions to ask. Really, the only thing tht makes sense is to strive for greater collective enlightenment.",
            "In terms of the Internet, it's like humanity acquiring a collective nervous system. Whereas previously we were more like a [?], like a collection of cells that communicated by diffusion. With the advent of the Internet, it was suddenly like we got a nervous system. It's a hugely impactful thing.",
            "I take the position that I'm always to some degree wrong, and the aspiration is to be less wrong.",
            "I could go and buy one of the islands in the Bahamas and turn it into my personal fiefdom, but I am much more interested in trying to build and create a new company.",
            "It’s pretty hard to get to another star system. Alpha Centauri is four light years away, so if you go at 10 per cent of the speed of light, it’s going to take you 40 years, and that’s assuming you can instantly reach that speed, which isn’t going to be the case. You have to accelerate. You have to build up to 20 or 30 per cent and then slow down, assuming you want to stay at Alpha Centauri and not go zipping past. It’s just hard. With current life spans, you need generational ships. You need antimatter drives, because that’s the most mass-efficient. It’s doable, but it’s super slow.",
            "I would like to die on Mars. Just not on impact.",
            "I'm not trying to be anyone's savior. I just try to think about the future and not be sad",
            "It's OK to have your eggs in one basket as long as you control what happens to that basket.",
            "I really like computer games, but then if I made really great computer games, how much effect would that have on the world.",
            "If something is important enough, you do it even if the odds aren't in your favor.",
            "If you're not concerned about AI safety, you should be. Vastly more risk than North Korea.",
            "If humanity is to become multi-planetary, the fundamental breakthrough that needs to occur in rocketry is a rapidly and completely reusable rocket ... achieving it would be on a par with what the Wright brothers did. It’s the fundamental thing that’s necessary for humanity to become a space-faring civilization. America would never have been colonized if ships weren’t reusable.",
            "I mean, I think that if people are concerned about volatility, they should definitely not buy our stock. I’m not here [on an earnings call] to convince you to buy [Tesla] stock. Do not buy it if volatility is scary. There you go.",
            "I think you should always bear in mind that entropy is not on your side.",
            "If something is important enough, even if the odds are against you, you should still do it.",
            "If something is important enough, you should try. Even if the probable outcome is failure.",
            "I came to the conclusion that we should aspire to increase the scope and scale of human consciousness in order to better understand what questions to ask. Really, the only thing that makes sense is to strive for greater collective enlightenment.",
            "If you get up in the morning and think the future is going to be better, it is a bright day. Otherwise, it’s not.",
            "If you’re trying to create a company, it’s like baking a cake. You have to have all the ingredients in the right proportion.",
            "I wouldn’t say I have a lack of fear. In fact, I’d like my fear emotion to be less because it’s very distracting and fries my nervous system.",
            "If you go back a few hundred years, what we take for granted today would seem like magic – being able to talk to people over long distances, to transmit images, flying, accessing vast amounts of data like an oracle. These are all things that would have been considered magic a few hundred years ago.",
            "It is a mistake to hire huge numbers of people to get a complicated job done. Numbers will never compensate for talent in getting the right answer (two people who don’t know something are no better than one), will tend to slow down progress, and will make the task incredibly expensive.",
            "I think it is possible for ordinary people to choose to be extraordinary.",
            "It’s OK to have your eggs in one basket as long as you control what happens to that basket.",
            "I could either watch it happen or be a part of it",
            "I think most of the important stuff on the Internet has been built.",
            "I think it’s very important to have a feedback loop, where you’re constantly thinking about what you’ve done and how you could be doing it better. I think that’s the single best piece of advice: constantly think about how you could be doing things better and questioning yourself.",
            "It’s very important to like the people you work with, otherwise life [and] your job is gonna be quite miserable.",
            "I always have optimism, but I’m realistic. It was not with the expectation of great success that I started Tesla or SpaceX.... It’s just that I thought they were important enough to do anyway.",
            "I think life on Earth must be about more than just solving problems... It’s got to be something inspiring, even if it is vicarious.",
            "If you want to grow a giant redwood, you need to make sure the seeds are OK, nurture the sapling and work out what might potentially stop it from growing all the way along. Anything that breaks it at any point stops that growth.",
            "I always have optimism, but I’m realistic. It was not with the expectation of great success that I started Tesla or SpaceX. It’s just that I thought they were important enough to do anyway.",
            "I could either watch it happen or be a part of it.",
            "Life is too short for long-term grudges.",
            "Let’s think beyond the normal stuff and have an environment where that sort of thinking is encouraged and rewarded and where it’s okay to fail as well. Because when you try new things, you try this idea, that idea... well a large number of them are not gonna work, and that has to be okay. If every time somebody comes up with an idea it has to be successful, you’re not gonna get people coming up with ideas.",
            "My proceeds from the PayPal acquisition were $180 million. I put $100 million in SpaceX, $70m in Tesla, and $10m in Solar City. I had to borrow money for rent.",
            "My motivation for all my companies has been to be involved in something that I thought would have a significant impact on the world.",
            "My biggest mistake is probably weighing too much on someone’s talent and not someone’s personality. I think it matters whether someone has a good heart.",
            "No, I don't ever give up. I'd have to be dead or completely incapacitated",
            "One of the biggest mistakes we made was trying to automate things that are super easy for a person to do, but super hard for a robot to do.",
            "One of the really tough things is figuring out what questions to ask. Once you figure out the question, then the answer is relatively easy.",
            "Optimism, pessimism, f*ck that – we’re going to make it happen.",
            "People work better when they know what the goal is and why. It is important that people look forward to coming to work in the morning and enjoy working.",
            "Patience is a virtue, and I’m learning patience. It’s a tough lesson.",
            "Persistence is very important. You should not give up unless you are forced to give up.",
            "People work better when they know what the goal is and why.",
            "People should pursue what they’re passionate about. That will make them happier than pretty much anything else.",
            "Really pay attention to negative feedback and solicit it, particularly from friends. ... Hardly anyone does that, and it’s incredibly helpful.",
            "Really, the only thing that makes sense is to strive for greater collective enlightenment.",
            "Some people don’t like change, but you need to embrace change if the alternative is disaster.",
            "Starting and growing a business is as much about the innovation, drive and determination of the people who do it as it is about the product they sell.",
            "Starting and growing a business is as much about the innovation, drive and determination of the people who do it as it is about the product they sell. Really, the only thing that makes sense is to strive for greater collective enlightenment.",
            "Some people don’t like change, but you need to embrace change as the alternative is disaster.",
            "Some people dont like change, but you need to embrace change if the alternative is disaster.",
            "The idea of lying on a beach as my main thing just sounds like the worst — it sounds horrible to me. I would go bonkers. I would have to be on serious drugs. I’d be super-duper bored. I like high intensity.",
            "The first step is to establish that something is possible then probability will occur.",
            "They were building a Ferrari for every launch, when it was possible that a Honda Accord might do the trick.",
            "The first step is to establish that something is possible; then probability will occur.",
            "The things that’s worth doing is trying to improve our understanding of the world and gain a better appreciation of the universe and not to worry too much about there being no meaning. And, you know, try and enjoy yourself. Because actually, life’s pretty good. It really is.",
            "Theres a tremendous bias against taking risks. Everyone is trying to optimize their ass-covering.",
            "When something is important enough, you do it even if the odds are not in your favour.",
            "Work like hell. I mean you just have to put in 80 to 100 hour weeks every week. [This] improves the odds of success. If other people are putting in 40 hour work weeks and you’re putting in 100 hour work weeks, then even if you’re doing the same thing you know that... you will achieve in 4 months what it takes them a year to achieve.",
            "Work like hell. I mean you just have to put in 80 to 100 hour weeks every week. [This] improves the odds of success.",
            "When something is important enough you do it even if the odds are not in your favor.",
            "When I was in college, I wanted to be involved in things that would change the world. Now I am.",
            "Why do you want to live? What’s the point? What inspires you? What do you love about the future? And if the future’s not including being out there among the stars and being a multi-planet species, it’s incredibly depressing if that’s not the future we’re going to have.",
            "Work like hell. I mean you just have to put in 80 to 100 hour weeks every week. This improves the odds of success.",
            "You should take the approach that you’re wrong. Your goal is to be less wrong.",
            "You get paid in direct proportion to the difficulty of problems you solve",
            "You need to live in a dome initially, but over time you could terraform Mars to look like Earth and eventually walk around outside without anything on... So it's a fixer-upper of a planet.",
            "You want to have a future where you’re expecting things to be better, not one where you’re expecting things to be worse.",
            "You have to be pretty driven to make it happen. Otherwise, you will just make yourself miserable.",
            "You shouldn’t do things differently just because they’re different. They need to be... better.",
            "You want to be extra rigorous about making the best possible thing you can. Find everything that’s wrong with it and fix it. Seek negative feedback, particularly from friends."
        ]
        await ctx.send(f"\"{random.choice(ELON)}\"")


def setup(bot):
    bot.add_cog(RandomCommands(bot))