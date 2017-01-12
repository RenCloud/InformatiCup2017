namespace GitRepoToJSON.Models
{
    /// <summary>
    /// Complete Data Object from all Api calls to create a JSON
    /// </summary>
    public struct JSONFullData
    {
        public long id;
        public string name;
        public string full_name;
        public int owner_id;
        public string description;
        public string readme;
        public Language[] language;
        public Repro[] repository;
        public bool truncated;
        public Commits[] commits;
        public Comments[] comments;
        public Issue[] issue;

        /// <summary>
        /// Constructor for a Full Data Object
        /// </summary>
        /// <param name="id">Id of the Repository</param>
        /// <param name="name">name of the Repository</param>
        /// <param name="fullName">full name of the Repository</param>
        /// <param name="ownerId">Owner ID</param>
        /// <param name="description">Desciption of the Repository</param>
        /// <param name="readme">Readme file of the Repository</param>
        /// <param name="language">Main (Most used) Language of Code in the Repository</param>
        /// <param name="repository">Path and Type of the Repository</param>
        /// <param name="truncated">Has the Repository to mutch ( don't know above 100.000 may) files and dirs</param>
        /// <param name="commits">Commits from Repository</param>
        /// <param name="comments">Comments from Repository</param>
        /// <param name="issue">Issue from Repository</param>
        public JSONFullData(long id, string name, string fullName, int ownerId, string description, string readme, Language[] language, Repro[] repository, bool truncated, Commits[] commits, Comments[] comments, Issue[] issue)
        {
            this.id = id;
            this.name = name;
            full_name = fullName;
            owner_id = ownerId;
            this.description = description;
            this.readme = readme;
            this.language = language;
            this.repository = repository;
            this.truncated = truncated;
            this.commits = commits;
            this.comments = comments;
            this.issue = issue;
        }
    }

    /// <summary>
    /// Language used within the Repo and his size
    /// </summary>
    public struct Language
    {
        public string lang;
        public long bytes;

        /// <summary>
        /// Constructor of an Language Object
        /// </summary>
        /// <param name="lang">Code Language</param>
        /// <param name="bytes">Sum of File sizes with this language</param>
        public Language(string lang, long bytes)
        {
            this.lang = lang;
            this.bytes = bytes;
        }
    }

    /// <summary>
    /// Repro type 
    /// </summary>
    public struct Repro
    {
        public string path;
        public string type;

        /// <summary>
        /// Constructor
        /// </summary>
        /// <param name="path">Path</param>
        /// <param name="type">Type</param>
        public Repro(string path, string type)
        {
            this.path = path;
            this.type = type;
        }
    }

    /// <summary>
    /// Commits Api Call Object
    /// </summary>
    public struct Commits
    {
        public Commit commit;
        public string author_login;
        public string committer_login;

        /// <summary>
        /// Constructor for an Commits Object with full data
        /// </summary>
        /// <param name="commit">Commit Object from Api call</param>
        /// <param name="authorLogin">Login Name of the Author</param>
        /// <param name="committerLogin">Login name of the Committer</param>
        public Commits(Commit commit, string authorLogin, string committerLogin)
        {
            this.commit = commit;
            author_login = authorLogin;
            committer_login = committerLogin;
        }
    }

    /// <summary>
    /// Commit Object from Api Call
    /// </summary>
    public struct Commit
    {
        public Author author;
        public Author commiter;
        public string message;

        /// <summary>
        /// Constructor for full Commit Object
        /// </summary>
        /// <param name="author">Comit Author Name</param>
        /// <param name="commiter">Commiter Name</param>
        /// <param name="message">Message of Commit</param>
        public Commit(Author author, Author commiter, string message)
        {
            this.author = author;
            this.commiter = commiter;
            this.message = message;
        }
    }

    /// <summary>
    /// Author Api Object
    /// </summary>
    public struct Author
    {
        public string name;
        public string email;

        /// <summary>
        /// Constructor for full Author Object
        /// </summary>
        /// <param name="name">Name of the Author </param>
        /// <param name="email">Email Address of Author</param>
        public Author(string name, string email)
        {
            this.name = name;
            this.email = email;
        }
    }

    /// <summary>
    /// Comments Api Object
    /// </summary>
    public struct Comments
    {
        public string body;
        public string path;
        public Author user;

        /// <summary>
        /// Constructor for full Comments Object
        /// </summary>
        /// <param name="body">Body Message</param>
        /// <param name="path">Path of Data that is Comment</param>
        /// <param name="user">User who is comment</param>
        public Comments(string body, string path, Author user)
        {
            this.body = body;
            this.path = path;
            this.user = user;
        }
    }

    /// <summary>
    /// Issue Api call Object
    /// </summary>
    public struct Issue
    {
        public string state;
        public string title;
        public string body;
        public Author user;

        /// <summary>
        /// Constructor for full Issue object
        /// </summary>
        /// <param name="state">State of Issue</param>
        /// <param name="title">Issue Title</param>
        /// <param name="body">Body of Issue</param>
        /// <param name="user">User that writes the Issue</param>
        public Issue(string state, string title, string body, Author user)
        {
            this.state = state;
            this.title = title;
            this.body = body;
            this.user = user;

        }
    }
}