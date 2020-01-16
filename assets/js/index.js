import '../sass/app.scss';
import axios from 'axios';
const runTests = () => {
	const generateTable = sites => {
		let innerHTML = "";
		const ok = '<i class="fas fa-check-circle" style="font-size: 1.5rem; color: green"></i>';
		const alert = '<i class="fas fa-exclamation" style="font-size: 1.5rem; color: red"></i>';

		for (let site of sites){
			site = JSON.parse(site);
			status = site.status ? ok : alert;
			innerHTML += '<tr>';
			innerHTML += '<th scope="row">' + site.title + '</th>';
			innerHTML += '<td>' + site.url + '</td>';
			innerHTML += '<td class="text-center">' + status + '</td>';
			innerHTML += '<td class="text-right pl-3">';
			innerHTML += '<a href="/delete-site?id=' + site.id + '" class="btn btn-danger">';
			innerHTML += 'Remove Site</a></td>';
			innerHTML += '</tr>';
		}
		const table = document.querySelector('#site-status-table');
		table.innerHTML = innerHTML;
	};
	const clearTable = () => {
		const table = document.querySelector('#site-status-table');
		table.innerHTML = '';	
	};

	const addLoader = () => {
		const loader = document.getElementsByClassName('lds-roller')[0];
		loader.classList.remove('d-none');
	};

	const removeLoader = () => {
		const loader = document.getElementsByClassName('lds-roller')[0];
		loader.classList.add('d-none');
	};

	clearTable();
	addLoader();
	axios.get('/site-status')
	.then(res => generateTable(res.data.sites))
	.then(removeLoader)
	.catch(e => console.log(e));
};

window.runTests = runTests;