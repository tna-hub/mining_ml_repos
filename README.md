
# Mining machine learning repositories
``` For instructions to execute the extraction, please read help.txt file ```

This project aims to mining github machine learning repositories in order to understand how they deal with datasets. It is part of of a bigger project having three reseach questions:

  - RQ1: What are the main libraries used in these projects?
  - RQ2: How  do developers deal  with  datasets  in  ML projects?
  - RQ3: How  do ML projects evolve?

# Dataset
We analysed repositories from the Paper Of Code project which put together machine learning research papers with their corresponding github repository. We then filtered it to get only repos writen in python language.

a) Downloaded the paper of code files (json)

b) Extracted, through github API, the repos main language and the number of commits.the repositories with python as main language

c)We filtered by removing duplicates and project that didn't have python as main language. Duplicates are projects that have the same github link. These are usually different versions of the paper but still linked to the same github repository.

d) The result is a csv file with headers id; unique id of the repository, link; github link of the repo and nb_commits: total commits in the repository.

e) For each commits, we extracted some information we think are relevant for the analysis, and store them to a postgresql database.

<div>
<a name="user-content-layout1">
</a></div><a name="user-content-layout1">
</a><div><a name="user-content-layout1">
</a><p><a name="user-content-layout1"><br>
</a></p><div><a name="user-content-layout1"></a><div><a name="user-content-layout1"></a><a name="user-content-public.commit_modifications"></a><h5><a name="user-content-public.commit_modifications"></a><a id="user-content-table-commit_modifications" class="anchor" aria-hidden="true" href="#table-commit_modifications"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.775 3.275C7.64252 3.41717 7.57039 3.60522 7.57382 3.79952C7.57725 3.99382 7.65596 4.1792 7.79337 4.31662C7.93079 4.45403 8.11617 4.53274 8.31047 4.53617C8.50477 4.5396 8.69282 4.46748 8.835 4.335L10.085 3.085C10.2708 2.89918 10.4914 2.75177 10.7342 2.65121C10.977 2.55064 11.2372 2.49888 11.5 2.49888C11.7628 2.49888 12.023 2.55064 12.2658 2.65121C12.5086 2.75177 12.7292 2.89918 12.915 3.085C13.1008 3.27082 13.2482 3.49142 13.3488 3.7342C13.4493 3.97699 13.5011 4.23721 13.5011 4.5C13.5011 4.76279 13.4493 5.023 13.3488 5.26579C13.2482 5.50857 13.1008 5.72917 12.915 5.915L10.415 8.415C10.2292 8.60095 10.0087 8.74847 9.76588 8.84911C9.52308 8.94976 9.26283 9.00157 9 9.00157C8.73716 9.00157 8.47691 8.94976 8.23411 8.84911C7.99132 8.74847 7.77074 8.60095 7.585 8.415C7.44282 8.28252 7.25477 8.21039 7.06047 8.21382C6.86617 8.21725 6.68079 8.29596 6.54337 8.43337C6.40596 8.57079 6.32725 8.75617 6.32382 8.95047C6.32039 9.14477 6.39252 9.33282 6.525 9.475C6.85001 9.80004 7.23586 10.0579 7.66052 10.2338C8.08518 10.4097 8.54034 10.5002 9 10.5002C9.45965 10.5002 9.91481 10.4097 10.3395 10.2338C10.7641 10.0579 11.15 9.80004 11.475 9.475L13.975 6.975C14.6314 6.31858 15.0002 5.4283 15.0002 4.5C15.0002 3.57169 14.6314 2.68141 13.975 2.025C13.3186 1.36858 12.4283 0.999817 11.5 0.999817C10.5717 0.999817 9.68141 1.36858 9.02499 2.025L7.775 3.275ZM3.085 12.915C2.89904 12.7292 2.75152 12.5087 2.65088 12.2659C2.55023 12.0231 2.49842 11.7628 2.49842 11.5C2.49842 11.2372 2.55023 10.9769 2.65088 10.7341C2.75152 10.4913 2.89904 10.2707 3.085 10.085L5.585 7.585C5.77074 7.39904 5.99132 7.25152 6.23411 7.15088C6.47691 7.05023 6.73716 6.99842 7 6.99842C7.26283 6.99842 7.52308 7.05023 7.76588 7.15088C8.00867 7.25152 8.22925 7.39904 8.415 7.585C8.55717 7.71748 8.74522 7.7896 8.93952 7.78617C9.13382 7.78274 9.3192 7.70403 9.45662 7.56662C9.59403 7.4292 9.67274 7.24382 9.67617 7.04952C9.6796 6.85522 9.60748 6.66717 9.475 6.525C9.14999 6.19995 8.76413 5.94211 8.33947 5.7662C7.91481 5.59029 7.45965 5.49974 7 5.49974C6.54034 5.49974 6.08518 5.59029 5.66052 5.7662C5.23586 5.94211 4.85001 6.19995 4.525 6.525L2.025 9.02499C1.36858 9.68141 0.999817 10.5717 0.999817 11.5C0.999817 12.4283 1.36858 13.3186 2.025 13.975C2.68141 14.6314 3.57169 15.0002 4.5 15.0002C5.4283 15.0002 6.31858 14.6314 6.975 13.975L8.225 12.725C8.35748 12.5828 8.4296 12.3948 8.42617 12.2005C8.42274 12.0062 8.34403 11.8208 8.20662 11.6834C8.0692 11.546 7.88382 11.4672 7.68952 11.4638C7.49522 11.4604 7.30717 11.5325 7.165 11.665L5.915 12.915C5.72925 13.1009 5.50867 13.2485 5.26588 13.3491C5.02308 13.4498 4.76283 13.5016 4.5 13.5016C4.23716 13.5016 3.97691 13.4498 3.73411 13.3491C3.49132 13.2485 3.27074 13.1009 3.085 12.915Z"></path></svg></a>Table commit_modifications</h5><p></p>
<table>
<thead>
<tr><th>Idx</th><th>Field Name</th><th>Data Type</th><th>Description</th></tr>
</thead>
<tbody>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.commit_modifications_id">id</a></td>
		<td> integer GENERATED BY DEFAULT AS IDENTITY  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.commit_modifications_file_id">file_id</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.commit_modifications_change_type">change_type</a></td>
		<td> varchar  </td>
		<td>  </td>
	</tr>
	<tr>
		<td></td>
		<td><a name="user-content-public.commit_modifications_commit_id">commit_id</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
</tbody>
</table></div></div>
<br>
<div><div><a name="user-content-public.commits"></a><h5><a name="user-content-public.commits"></a><a id="user-content-table-commits" class="anchor" aria-hidden="true" href="#table-commits"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.775 3.275C7.64252 3.41717 7.57039 3.60522 7.57382 3.79952C7.57725 3.99382 7.65596 4.1792 7.79337 4.31662C7.93079 4.45403 8.11617 4.53274 8.31047 4.53617C8.50477 4.5396 8.69282 4.46748 8.835 4.335L10.085 3.085C10.2708 2.89918 10.4914 2.75177 10.7342 2.65121C10.977 2.55064 11.2372 2.49888 11.5 2.49888C11.7628 2.49888 12.023 2.55064 12.2658 2.65121C12.5086 2.75177 12.7292 2.89918 12.915 3.085C13.1008 3.27082 13.2482 3.49142 13.3488 3.7342C13.4493 3.97699 13.5011 4.23721 13.5011 4.5C13.5011 4.76279 13.4493 5.023 13.3488 5.26579C13.2482 5.50857 13.1008 5.72917 12.915 5.915L10.415 8.415C10.2292 8.60095 10.0087 8.74847 9.76588 8.84911C9.52308 8.94976 9.26283 9.00157 9 9.00157C8.73716 9.00157 8.47691 8.94976 8.23411 8.84911C7.99132 8.74847 7.77074 8.60095 7.585 8.415C7.44282 8.28252 7.25477 8.21039 7.06047 8.21382C6.86617 8.21725 6.68079 8.29596 6.54337 8.43337C6.40596 8.57079 6.32725 8.75617 6.32382 8.95047C6.32039 9.14477 6.39252 9.33282 6.525 9.475C6.85001 9.80004 7.23586 10.0579 7.66052 10.2338C8.08518 10.4097 8.54034 10.5002 9 10.5002C9.45965 10.5002 9.91481 10.4097 10.3395 10.2338C10.7641 10.0579 11.15 9.80004 11.475 9.475L13.975 6.975C14.6314 6.31858 15.0002 5.4283 15.0002 4.5C15.0002 3.57169 14.6314 2.68141 13.975 2.025C13.3186 1.36858 12.4283 0.999817 11.5 0.999817C10.5717 0.999817 9.68141 1.36858 9.02499 2.025L7.775 3.275ZM3.085 12.915C2.89904 12.7292 2.75152 12.5087 2.65088 12.2659C2.55023 12.0231 2.49842 11.7628 2.49842 11.5C2.49842 11.2372 2.55023 10.9769 2.65088 10.7341C2.75152 10.4913 2.89904 10.2707 3.085 10.085L5.585 7.585C5.77074 7.39904 5.99132 7.25152 6.23411 7.15088C6.47691 7.05023 6.73716 6.99842 7 6.99842C7.26283 6.99842 7.52308 7.05023 7.76588 7.15088C8.00867 7.25152 8.22925 7.39904 8.415 7.585C8.55717 7.71748 8.74522 7.7896 8.93952 7.78617C9.13382 7.78274 9.3192 7.70403 9.45662 7.56662C9.59403 7.4292 9.67274 7.24382 9.67617 7.04952C9.6796 6.85522 9.60748 6.66717 9.475 6.525C9.14999 6.19995 8.76413 5.94211 8.33947 5.7662C7.91481 5.59029 7.45965 5.49974 7 5.49974C6.54034 5.49974 6.08518 5.59029 5.66052 5.7662C5.23586 5.94211 4.85001 6.19995 4.525 6.525L2.025 9.02499C1.36858 9.68141 0.999817 10.5717 0.999817 11.5C0.999817 12.4283 1.36858 13.3186 2.025 13.975C2.68141 14.6314 3.57169 15.0002 4.5 15.0002C5.4283 15.0002 6.31858 14.6314 6.975 13.975L8.225 12.725C8.35748 12.5828 8.4296 12.3948 8.42617 12.2005C8.42274 12.0062 8.34403 11.8208 8.20662 11.6834C8.0692 11.546 7.88382 11.4672 7.68952 11.4638C7.49522 11.4604 7.30717 11.5325 7.165 11.665L5.915 12.915C5.72925 13.1009 5.50867 13.2485 5.26588 13.3491C5.02308 13.4498 4.76283 13.5016 4.5 13.5016C4.23716 13.5016 3.97691 13.4498 3.73411 13.3491C3.49132 13.2485 3.27074 13.1009 3.085 12.915Z"></path></svg></a>Table commits</h5>
<table>
<thead>
<tr><th>Idx</th><th>Field Name</th><th>Data Type</th><th>Description</th></tr>
</thead>
<tbody>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.commits_id">id</a></td>
		<td> integer GENERATED BY DEFAULT AS IDENTITY  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.commits_repo_id">repo_id</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.commits_sha">sha</a></td>
		<td> varchar  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.commits_commit_date">commit_date</a></td>
		<td> timestamp  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.commits_author_name">author_name</a></td>
		<td> varchar  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.commits_author_email">author_email</a></td>
		<td> varchar  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.commits_total_modifs">total_modifs</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
</tbody>
</table></div></div>
<p><br></p>
<div><div><a name="user-content-public.datasets"></a><h5><a name="user-content-public.datasets"></a><a id="user-content-table-datasets" class="anchor" aria-hidden="true" href="#table-datasets"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.775 3.275C7.64252 3.41717 7.57039 3.60522 7.57382 3.79952C7.57725 3.99382 7.65596 4.1792 7.79337 4.31662C7.93079 4.45403 8.11617 4.53274 8.31047 4.53617C8.50477 4.5396 8.69282 4.46748 8.835 4.335L10.085 3.085C10.2708 2.89918 10.4914 2.75177 10.7342 2.65121C10.977 2.55064 11.2372 2.49888 11.5 2.49888C11.7628 2.49888 12.023 2.55064 12.2658 2.65121C12.5086 2.75177 12.7292 2.89918 12.915 3.085C13.1008 3.27082 13.2482 3.49142 13.3488 3.7342C13.4493 3.97699 13.5011 4.23721 13.5011 4.5C13.5011 4.76279 13.4493 5.023 13.3488 5.26579C13.2482 5.50857 13.1008 5.72917 12.915 5.915L10.415 8.415C10.2292 8.60095 10.0087 8.74847 9.76588 8.84911C9.52308 8.94976 9.26283 9.00157 9 9.00157C8.73716 9.00157 8.47691 8.94976 8.23411 8.84911C7.99132 8.74847 7.77074 8.60095 7.585 8.415C7.44282 8.28252 7.25477 8.21039 7.06047 8.21382C6.86617 8.21725 6.68079 8.29596 6.54337 8.43337C6.40596 8.57079 6.32725 8.75617 6.32382 8.95047C6.32039 9.14477 6.39252 9.33282 6.525 9.475C6.85001 9.80004 7.23586 10.0579 7.66052 10.2338C8.08518 10.4097 8.54034 10.5002 9 10.5002C9.45965 10.5002 9.91481 10.4097 10.3395 10.2338C10.7641 10.0579 11.15 9.80004 11.475 9.475L13.975 6.975C14.6314 6.31858 15.0002 5.4283 15.0002 4.5C15.0002 3.57169 14.6314 2.68141 13.975 2.025C13.3186 1.36858 12.4283 0.999817 11.5 0.999817C10.5717 0.999817 9.68141 1.36858 9.02499 2.025L7.775 3.275ZM3.085 12.915C2.89904 12.7292 2.75152 12.5087 2.65088 12.2659C2.55023 12.0231 2.49842 11.7628 2.49842 11.5C2.49842 11.2372 2.55023 10.9769 2.65088 10.7341C2.75152 10.4913 2.89904 10.2707 3.085 10.085L5.585 7.585C5.77074 7.39904 5.99132 7.25152 6.23411 7.15088C6.47691 7.05023 6.73716 6.99842 7 6.99842C7.26283 6.99842 7.52308 7.05023 7.76588 7.15088C8.00867 7.25152 8.22925 7.39904 8.415 7.585C8.55717 7.71748 8.74522 7.7896 8.93952 7.78617C9.13382 7.78274 9.3192 7.70403 9.45662 7.56662C9.59403 7.4292 9.67274 7.24382 9.67617 7.04952C9.6796 6.85522 9.60748 6.66717 9.475 6.525C9.14999 6.19995 8.76413 5.94211 8.33947 5.7662C7.91481 5.59029 7.45965 5.49974 7 5.49974C6.54034 5.49974 6.08518 5.59029 5.66052 5.7662C5.23586 5.94211 4.85001 6.19995 4.525 6.525L2.025 9.02499C1.36858 9.68141 0.999817 10.5717 0.999817 11.5C0.999817 12.4283 1.36858 13.3186 2.025 13.975C2.68141 14.6314 3.57169 15.0002 4.5 15.0002C5.4283 15.0002 6.31858 14.6314 6.975 13.975L8.225 12.725C8.35748 12.5828 8.4296 12.3948 8.42617 12.2005C8.42274 12.0062 8.34403 11.8208 8.20662 11.6834C8.0692 11.546 7.88382 11.4672 7.68952 11.4638C7.49522 11.4604 7.30717 11.5325 7.165 11.665L5.915 12.915C5.72925 13.1009 5.50867 13.2485 5.26588 13.3491C5.02308 13.4498 4.76283 13.5016 4.5 13.5016C4.23716 13.5016 3.97691 13.4498 3.73411 13.3491C3.49132 13.2485 3.27074 13.1009 3.085 12.915Z"></path></svg></a>Table datasets</h5>
<table>
<thead>
<tr><th>Idx</th><th>Field Name</th><th>Data Type</th><th>Description</th></tr>
</thead>
<tbody>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.datasets_id">id</a></td>
		<td> integer GENERATED BY DEFAULT AS IDENTITY  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.datasets_element_id">element_id</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.datasets_heuristic">heuristic</a></td>
		<td> varchar(2)  </td>
		<td> The heuristic used to identify as dataset </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.datasets_file_mention">file_mention</a></td>
		<td> integer  </td>
		<td> The file where the dataset is loaded </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.datasets_repo_id">repo_id</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
</tbody>
</table></div></div>
<p><br></p>
<div><div><a name="user-content-public.element"></a><h5><a name="user-content-public.element"></a><a id="user-content-table-element" class="anchor" aria-hidden="true" href="#table-element"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.775 3.275C7.64252 3.41717 7.57039 3.60522 7.57382 3.79952C7.57725 3.99382 7.65596 4.1792 7.79337 4.31662C7.93079 4.45403 8.11617 4.53274 8.31047 4.53617C8.50477 4.5396 8.69282 4.46748 8.835 4.335L10.085 3.085C10.2708 2.89918 10.4914 2.75177 10.7342 2.65121C10.977 2.55064 11.2372 2.49888 11.5 2.49888C11.7628 2.49888 12.023 2.55064 12.2658 2.65121C12.5086 2.75177 12.7292 2.89918 12.915 3.085C13.1008 3.27082 13.2482 3.49142 13.3488 3.7342C13.4493 3.97699 13.5011 4.23721 13.5011 4.5C13.5011 4.76279 13.4493 5.023 13.3488 5.26579C13.2482 5.50857 13.1008 5.72917 12.915 5.915L10.415 8.415C10.2292 8.60095 10.0087 8.74847 9.76588 8.84911C9.52308 8.94976 9.26283 9.00157 9 9.00157C8.73716 9.00157 8.47691 8.94976 8.23411 8.84911C7.99132 8.74847 7.77074 8.60095 7.585 8.415C7.44282 8.28252 7.25477 8.21039 7.06047 8.21382C6.86617 8.21725 6.68079 8.29596 6.54337 8.43337C6.40596 8.57079 6.32725 8.75617 6.32382 8.95047C6.32039 9.14477 6.39252 9.33282 6.525 9.475C6.85001 9.80004 7.23586 10.0579 7.66052 10.2338C8.08518 10.4097 8.54034 10.5002 9 10.5002C9.45965 10.5002 9.91481 10.4097 10.3395 10.2338C10.7641 10.0579 11.15 9.80004 11.475 9.475L13.975 6.975C14.6314 6.31858 15.0002 5.4283 15.0002 4.5C15.0002 3.57169 14.6314 2.68141 13.975 2.025C13.3186 1.36858 12.4283 0.999817 11.5 0.999817C10.5717 0.999817 9.68141 1.36858 9.02499 2.025L7.775 3.275ZM3.085 12.915C2.89904 12.7292 2.75152 12.5087 2.65088 12.2659C2.55023 12.0231 2.49842 11.7628 2.49842 11.5C2.49842 11.2372 2.55023 10.9769 2.65088 10.7341C2.75152 10.4913 2.89904 10.2707 3.085 10.085L5.585 7.585C5.77074 7.39904 5.99132 7.25152 6.23411 7.15088C6.47691 7.05023 6.73716 6.99842 7 6.99842C7.26283 6.99842 7.52308 7.05023 7.76588 7.15088C8.00867 7.25152 8.22925 7.39904 8.415 7.585C8.55717 7.71748 8.74522 7.7896 8.93952 7.78617C9.13382 7.78274 9.3192 7.70403 9.45662 7.56662C9.59403 7.4292 9.67274 7.24382 9.67617 7.04952C9.6796 6.85522 9.60748 6.66717 9.475 6.525C9.14999 6.19995 8.76413 5.94211 8.33947 5.7662C7.91481 5.59029 7.45965 5.49974 7 5.49974C6.54034 5.49974 6.08518 5.59029 5.66052 5.7662C5.23586 5.94211 4.85001 6.19995 4.525 6.525L2.025 9.02499C1.36858 9.68141 0.999817 10.5717 0.999817 11.5C0.999817 12.4283 1.36858 13.3186 2.025 13.975C2.68141 14.6314 3.57169 15.0002 4.5 15.0002C5.4283 15.0002 6.31858 14.6314 6.975 13.975L8.225 12.725C8.35748 12.5828 8.4296 12.3948 8.42617 12.2005C8.42274 12.0062 8.34403 11.8208 8.20662 11.6834C8.0692 11.546 7.88382 11.4672 7.68952 11.4638C7.49522 11.4604 7.30717 11.5325 7.165 11.665L5.915 12.915C5.72925 13.1009 5.50867 13.2485 5.26588 13.3491C5.02308 13.4498 4.76283 13.5016 4.5 13.5016C4.23716 13.5016 3.97691 13.4498 3.73411 13.3491C3.49132 13.2485 3.27074 13.1009 3.085 12.915Z"></path></svg></a>Table element</h5>
<p>Information of files of folders in the repositories</p>
<table>
<thead>
<tr><th>Idx</th><th>Field Name</th><th>Data Type</th><th>Description</th></tr>
</thead>
<tbody>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.element_id">id</a></td>
		<td> integer GENERATED BY DEFAULT AS IDENTITY  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.element_name">name</a></td>
		<td> varchar(500)  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.element_is_code_file">is_code_file</a></td>
		<td> bool  </td>
		<td> Set to True or False if file has code or not </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.element_ast">ast</a></td>
		<td> json  </td>
		<td> json ast of the file's code </td>
	</tr>
	<tr>
		<td></td>
		<td><a name="user-content-public.element_repo_id">repo_id</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.element_is_folder">is_folder</a></td>
		<td> bool  </td>
		<td> True if it is a folder, false if it is not </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.element_extension">extension</a></td>
		<td> varchar  </td>
		<td>  </td>
	</tr>
</tbody>
</table></div></div>
<p><br></p>
<div><div><a name="user-content-public.repos"></a><h5><a name="user-content-public.repos"></a><a id="user-content-table-repos" class="anchor" aria-hidden="true" href="#table-repos"><svg class="octicon octicon-link" viewBox="0 0 16 16" version="1.1" width="16" height="16" aria-hidden="true"><path fill-rule="evenodd" clip-rule="evenodd" d="M7.775 3.275C7.64252 3.41717 7.57039 3.60522 7.57382 3.79952C7.57725 3.99382 7.65596 4.1792 7.79337 4.31662C7.93079 4.45403 8.11617 4.53274 8.31047 4.53617C8.50477 4.5396 8.69282 4.46748 8.835 4.335L10.085 3.085C10.2708 2.89918 10.4914 2.75177 10.7342 2.65121C10.977 2.55064 11.2372 2.49888 11.5 2.49888C11.7628 2.49888 12.023 2.55064 12.2658 2.65121C12.5086 2.75177 12.7292 2.89918 12.915 3.085C13.1008 3.27082 13.2482 3.49142 13.3488 3.7342C13.4493 3.97699 13.5011 4.23721 13.5011 4.5C13.5011 4.76279 13.4493 5.023 13.3488 5.26579C13.2482 5.50857 13.1008 5.72917 12.915 5.915L10.415 8.415C10.2292 8.60095 10.0087 8.74847 9.76588 8.84911C9.52308 8.94976 9.26283 9.00157 9 9.00157C8.73716 9.00157 8.47691 8.94976 8.23411 8.84911C7.99132 8.74847 7.77074 8.60095 7.585 8.415C7.44282 8.28252 7.25477 8.21039 7.06047 8.21382C6.86617 8.21725 6.68079 8.29596 6.54337 8.43337C6.40596 8.57079 6.32725 8.75617 6.32382 8.95047C6.32039 9.14477 6.39252 9.33282 6.525 9.475C6.85001 9.80004 7.23586 10.0579 7.66052 10.2338C8.08518 10.4097 8.54034 10.5002 9 10.5002C9.45965 10.5002 9.91481 10.4097 10.3395 10.2338C10.7641 10.0579 11.15 9.80004 11.475 9.475L13.975 6.975C14.6314 6.31858 15.0002 5.4283 15.0002 4.5C15.0002 3.57169 14.6314 2.68141 13.975 2.025C13.3186 1.36858 12.4283 0.999817 11.5 0.999817C10.5717 0.999817 9.68141 1.36858 9.02499 2.025L7.775 3.275ZM3.085 12.915C2.89904 12.7292 2.75152 12.5087 2.65088 12.2659C2.55023 12.0231 2.49842 11.7628 2.49842 11.5C2.49842 11.2372 2.55023 10.9769 2.65088 10.7341C2.75152 10.4913 2.89904 10.2707 3.085 10.085L5.585 7.585C5.77074 7.39904 5.99132 7.25152 6.23411 7.15088C6.47691 7.05023 6.73716 6.99842 7 6.99842C7.26283 6.99842 7.52308 7.05023 7.76588 7.15088C8.00867 7.25152 8.22925 7.39904 8.415 7.585C8.55717 7.71748 8.74522 7.7896 8.93952 7.78617C9.13382 7.78274 9.3192 7.70403 9.45662 7.56662C9.59403 7.4292 9.67274 7.24382 9.67617 7.04952C9.6796 6.85522 9.60748 6.66717 9.475 6.525C9.14999 6.19995 8.76413 5.94211 8.33947 5.7662C7.91481 5.59029 7.45965 5.49974 7 5.49974C6.54034 5.49974 6.08518 5.59029 5.66052 5.7662C5.23586 5.94211 4.85001 6.19995 4.525 6.525L2.025 9.02499C1.36858 9.68141 0.999817 10.5717 0.999817 11.5C0.999817 12.4283 1.36858 13.3186 2.025 13.975C2.68141 14.6314 3.57169 15.0002 4.5 15.0002C5.4283 15.0002 6.31858 14.6314 6.975 13.975L8.225 12.725C8.35748 12.5828 8.4296 12.3948 8.42617 12.2005C8.42274 12.0062 8.34403 11.8208 8.20662 11.6834C8.0692 11.546 7.88382 11.4672 7.68952 11.4638C7.49522 11.4604 7.30717 11.5325 7.165 11.665L5.915 12.915C5.72925 13.1009 5.50867 13.2485 5.26588 13.3491C5.02308 13.4498 4.76283 13.5016 4.5 13.5016C4.23716 13.5016 3.97691 13.4498 3.73411 13.3491C3.49132 13.2485 3.27074 13.1009 3.085 12.915Z"></path></svg></a>Table repos</h5>
<p>Repositories to analyse</p>
<table>
<thead>
<tr><th>Idx</th><th>Field Name</th><th>Data Type</th><th>Description</th></tr>
</thead>
<tbody>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.repos_id">id</a></td>
		<td> integer  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>*</td>
		<td><a name="user-content-public.repos_link">link</a></td>
		<td> varchar(5000)  </td>
		<td> Github link </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.repos_nb_commits">nb_commits</a></td>
		<td> integer  </td>
		<td> Total commits in the repository </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.repos_name">name</a></td>
		<td> varchar(500)  </td>
		<td>  </td>
	</tr>
	<tr>
		<td>&nbsp;</td>
		<td><a name="user-content-public.repos_folder_name">folder_name</a></td>
		<td> varchar(500)  </td>
		<td>  </td>
	</tr>
</tbody>
</table></div></div>
</div>
<br>
f) For RQ3, it may be interesting to assess the number of commits as another filtering criteria. Remove projects with less than x commits to keep only projects with the sufficient amount of commits.
For confidenttiality, researchers somethimes develop their code out of Github or in a private Repository, then once the paper is published, they then pull all the code into one or few commits to Github.
This removes all the medatadata associated to the project evolution and makes the project impossible to mine.


# Method

Given the fact that there are several ways to store data and that GitHub keeps tracks of changes in the project through files, we study how datafiles  are stored as and how they can impact the evolution of the repository.

## RQ1

Using python ast, we extracted the imported libraries from each repository, then analysed how these libraries are used in all the repositories using association mining

## RQ2
We developed some heuristics to identify dataset:
  1) h1: file and folder name: Any non code file or folder name containing the String ``` *data*``` is considered as storing data files.
  ) h2: Non code file  or folder name is loaded in the code: Using python ast, we find all mentions of non-code files and folder names in code files. Ignoring standard files like README.md, setyp.py, requirements.txt and files ending with extensions "", ".md", ".yml", ".sh", ".h"
  
  It may be interesting to find out if the data is mentioned as input or output dataset by using the function calling it. But due to the disparity and the huge number of possibilities to use data (custom function, function open(), library function), this may a hard task that will need time to identify at an interesting number of possibilities that won't bias the results. We can use the libraries from rq1 and checck the functions each library implemented to load datasets, along with built in funtion open('filename', 'mode') to determine is the dataset is loaded as input of output.
  
  ## RQ3
  the third rq is to assess how the datafiles and the code evolve together.
For that, for each identified datafile (a file from the repo is identified as datafile according to the heuristics of the rq2), we checked all the commits modifying that file (C). We then looked at how many time a file appears in the commits. Let's say the file "data.csv" has been modified n=10 times (there are ten commits where that file appears). for each commit C[i] in C, we checked all the files modified by that commit. Let's call C[n][j] the jth file of the commit commit C[i]. then we check the presence of C[i][j] in all the commits (from 0 to 10) and count how many times we found that file.

(Not yet done) Need to use a mathematical method combining the number of commits and the occurence of the file in the commits to asses what is the treshold from wich a file is correlated to another file in its evolution. Also may be interesting to check if  the reverse is true (if a correlated to b implies b is correlated to a)

