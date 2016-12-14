using Octokit;
using System.Collections.Generic;

namespace GitRepoToJSON.Models {
    public class ViewRepoOverview {
        public ViewRepoOverview(Repo[] repositories)
        {
            Repositories = repositories;
        }

        public ViewRepoOverview(Repo[] repos, TreeResponse[] treeResponses)
        {
            Repositories = repos;
            Tree = treeResponses;
        }

        public ViewRepoOverview(Repo[] repos, TreeResponse[] treeResponses, Readme[] readmes, IReadOnlyList<RepositoryLanguage>[] readOnlyLists, IReadOnlyList<GitHubCommit>[] gitHubCommits)
        {
            Repositories = repos;
            Tree = treeResponses;
            Readmes = readmes;
            Languagen = readOnlyLists;
            CommitS = gitHubCommits;
        }

        public ViewRepoOverview(Repo[] repos, TreeResponse[] treeResponses, Readme[] readmes, IReadOnlyList<RepositoryLanguage>[] readOnlyLists, IReadOnlyList<GitHubCommit>[] gitHubCommits, string[] strings, IReadOnlyList<CommitComment>[] commitComments, IReadOnlyList<Octokit.Issue>[] issues)
        {
            Repositories = repos;
            Tree = treeResponses;
            Readmes = readmes;
            Languagen = readOnlyLists;
            CommitS = gitHubCommits;
            ReadmeCon = strings;
            Comments = commitComments;
            Issues = issues;
        }

        public Repo[] Repositories { get; private set; }
        public TreeResponse[] Tree { get; private set; }
        public Readme[] Readmes { get; private set; }
        public IReadOnlyList<RepositoryLanguage>[] Languagen { get; private set; }
        public IReadOnlyList<GitHubCommit>[] CommitS { get; private set; }
        public string[] ReadmeCon { get; private set; }
        public IReadOnlyList<CommitComment>[] Comments { get; private set; }
        public IReadOnlyList<Octokit.Issue>[] Issues { get; private set; }

    }

}